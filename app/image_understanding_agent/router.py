"""FastAPI routes for the Image Understanding Agent."""

from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, status

from app.image_understanding_agent.image_understanding_agent_engine import (
    normalize_image_id,
)
from app.image_understanding_agent.schemas import (
    ImageUnderstandingRecord,
    ImageUnderstandingRecordResponse,
    UserImageUnderstandingAgentResponse,
)
from app.services.engine_registry import image_understanding_agent_engine

# Router exposed to FastAPI as image_understanding_agent_router in main.py.
image_understanding_agent_router = APIRouter(tags=["Image Understanding Agent"])


def parse_path_image_id(image_id: str) -> str:
    """Decode URL path image IDs so spaces work in GET, PUT, and DELETE."""
    return unquote(image_id.replace("+", " "))


@image_understanding_agent_router.post(
    "/image_understanding_agent/{user_id}",
    response_model=ImageUnderstandingRecordResponse,
    summary="Create image understanding record",
    description="Create a new image understanding record for the specified user.",
)
async def create_image_understanding_record(
    user_id: str,
    request: ImageUnderstandingRecord,
) -> ImageUnderstandingRecordResponse:
    """Create and return an image understanding record."""
    if image_understanding_agent_engine.image_id_exists(user_id, request.image_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Image understanding record already exists",
        )

    record = image_understanding_agent_engine.create_record(user_id, request)
    return ImageUnderstandingRecordResponse.from_record(record)


@image_understanding_agent_router.get(
    "/image_understanding_agent/{user_id}",
    response_model=UserImageUnderstandingAgentResponse,
    summary="Get all image understanding records",
    description="Return all image understanding records saved by the specified user.",
)
async def get_image_understanding_records(
    user_id: str,
) -> UserImageUnderstandingAgentResponse:
    """Return all image understanding records for a user."""
    records = image_understanding_agent_engine.get_records(user_id)
    return UserImageUnderstandingAgentResponse(
        user_id=user_id,
        image_understanding_records=[
            ImageUnderstandingRecordResponse.from_record(record)
            for record in records
        ],
    )


@image_understanding_agent_router.get(
    "/image_understanding_agent/{user_id}/{image_id}",
    response_model=ImageUnderstandingRecordResponse,
    summary="Get one image understanding record",
    description="Return one image understanding record identified by image ID.",
)
async def get_image_understanding_record(
    user_id: str,
    image_id: str,
) -> ImageUnderstandingRecordResponse:
    """Return a single image understanding record by ID."""
    decoded_id = parse_path_image_id(image_id)
    record = image_understanding_agent_engine.get_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image understanding record not found",
        )

    return ImageUnderstandingRecordResponse.from_record(record)


@image_understanding_agent_router.put(
    "/image_understanding_agent/{user_id}/{image_id}",
    response_model=ImageUnderstandingRecordResponse,
    status_code=status.HTTP_200_OK,
    summary="Update image understanding record",
    description="Replace an existing image understanding record with updated data.",
)
async def update_image_understanding_record(
    user_id: str,
    image_id: str,
    request: ImageUnderstandingRecord,
) -> ImageUnderstandingRecordResponse:
    """Update and return an image understanding record."""
    decoded_id = parse_path_image_id(image_id)

    if normalize_image_id(request.image_id) != normalize_image_id(decoded_id):
        if image_understanding_agent_engine.image_id_exists(user_id, request.image_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Image understanding record already exists",
            )

    record = image_understanding_agent_engine.update_record(
        user_id,
        decoded_id,
        request,
    )
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image understanding record not found",
        )

    return ImageUnderstandingRecordResponse.from_record(record)


@image_understanding_agent_router.delete(
    "/image_understanding_agent/{user_id}/{image_id}",
    response_model=ImageUnderstandingRecordResponse,
    summary="Delete image understanding record",
    description="Delete an image understanding record and return the removed record.",
)
async def delete_image_understanding_record(
    user_id: str,
    image_id: str,
) -> ImageUnderstandingRecordResponse:
    """Delete an image understanding record and return the deleted item."""
    decoded_id = parse_path_image_id(image_id)
    record = image_understanding_agent_engine.delete_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image understanding record not found",
        )

    return ImageUnderstandingRecordResponse.from_record(record)
