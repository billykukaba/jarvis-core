"""FastAPI routes for the Vision Agent."""

from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, status

from app.services.engine_registry import vision_agent_engine
from app.vision_agent.schemas import (
    UserVisionAgentResponse,
    VisionRecord,
    VisionRecordResponse,
)
from app.vision_agent.vision_agent_engine import normalize_image_id

# Router exposed to FastAPI as vision_agent_router in main.py.
vision_agent_router = APIRouter(tags=["Vision Agent"])


def parse_path_image_id(image_id: str) -> str:
    """Decode URL path image IDs so spaces work in GET, PUT, and DELETE."""
    return unquote(image_id.replace("+", " "))


@vision_agent_router.post(
    "/vision_agent/{user_id}",
    response_model=VisionRecordResponse,
    summary="Create vision record",
    description="Create a new vision analysis record for the specified user.",
)
async def create_vision_record(
    user_id: str,
    request: VisionRecord,
) -> VisionRecordResponse:
    """Create and return a vision record."""
    if vision_agent_engine.image_id_exists(user_id, request.image_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vision record already exists",
        )

    record = vision_agent_engine.create_record(user_id, request)
    return VisionRecordResponse.from_record(record)


@vision_agent_router.get(
    "/vision_agent/{user_id}",
    response_model=UserVisionAgentResponse,
    summary="Get all vision records",
    description="Return all vision analysis records saved by the specified user.",
)
async def get_vision_records(user_id: str) -> UserVisionAgentResponse:
    """Return all vision records for a user."""
    records = vision_agent_engine.get_records(user_id)
    return UserVisionAgentResponse(
        user_id=user_id,
        vision_records=[
            VisionRecordResponse.from_record(record) for record in records
        ],
    )


@vision_agent_router.get(
    "/vision_agent/{user_id}/{image_id}",
    response_model=VisionRecordResponse,
    summary="Get one vision record",
    description="Return one vision analysis record identified by image ID.",
)
async def get_vision_record(
    user_id: str,
    image_id: str,
) -> VisionRecordResponse:
    """Return a single vision record by ID."""
    decoded_id = parse_path_image_id(image_id)
    record = vision_agent_engine.get_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vision record not found",
        )

    return VisionRecordResponse.from_record(record)


@vision_agent_router.put(
    "/vision_agent/{user_id}/{image_id}",
    response_model=VisionRecordResponse,
    status_code=status.HTTP_200_OK,
    summary="Update vision record",
    description="Replace an existing vision analysis record with updated data.",
)
async def update_vision_record(
    user_id: str,
    image_id: str,
    request: VisionRecord,
) -> VisionRecordResponse:
    """Update and return a vision record."""
    decoded_id = parse_path_image_id(image_id)

    if normalize_image_id(request.image_id) != normalize_image_id(decoded_id):
        if vision_agent_engine.image_id_exists(user_id, request.image_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Vision record already exists",
            )

    record = vision_agent_engine.update_record(user_id, decoded_id, request)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vision record not found",
        )

    return VisionRecordResponse.from_record(record)


@vision_agent_router.delete(
    "/vision_agent/{user_id}/{image_id}",
    response_model=VisionRecordResponse,
    summary="Delete vision record",
    description="Delete a vision analysis record and return the removed record.",
)
async def delete_vision_record(
    user_id: str,
    image_id: str,
) -> VisionRecordResponse:
    """Delete a vision record and return the deleted item."""
    decoded_id = parse_path_image_id(image_id)
    record = vision_agent_engine.delete_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vision record not found",
        )

    return VisionRecordResponse.from_record(record)
