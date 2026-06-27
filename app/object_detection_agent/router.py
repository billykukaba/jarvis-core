"""FastAPI routes for the Object Detection Agent.

Detects and manages objects identified by Jarvis Vision System.
"""

from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, status

from app.object_detection_agent.object_detection_agent_engine import normalize_object_id
from app.object_detection_agent.schemas import (
    ObjectDetectionRecord,
    ObjectDetectionRecordResponse,
    UserObjectDetectionAgentResponse,
)
from app.services.engine_registry import object_detection_agent_engine

# Router exposed to FastAPI as object_detection_agent_router in main.py.
object_detection_agent_router = APIRouter(tags=["Object Detection Agent"])


def parse_path_object_id(object_id: str) -> str:
    """Decode URL path object IDs so spaces work in GET, PUT, and DELETE."""
    return unquote(object_id.replace("+", " "))


@object_detection_agent_router.post(
    "/object_detection_agent/{user_id}",
    response_model=ObjectDetectionRecordResponse,
    summary="Create object detection record",
    description=(
        "Create a new object detection record for the specified user. "
        "Detects and manages objects identified by Jarvis Vision System."
    ),
)
async def create_object_detection_record(
    user_id: str,
    request: ObjectDetectionRecord,
) -> ObjectDetectionRecordResponse:
    """Create and return an object detection record."""
    if object_detection_agent_engine.object_id_exists(user_id, request.object_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Object detection record already exists",
        )

    record = object_detection_agent_engine.create_record(user_id, request)
    return ObjectDetectionRecordResponse.from_record(record)


@object_detection_agent_router.get(
    "/object_detection_agent/{user_id}",
    response_model=UserObjectDetectionAgentResponse,
    summary="Get all object detection records",
    description=(
        "Return all object detection records saved by the specified user. "
        "Detects and manages objects identified by Jarvis Vision System."
    ),
)
async def get_object_detection_records(
    user_id: str,
) -> UserObjectDetectionAgentResponse:
    """Return all object detection records for a user."""
    records = object_detection_agent_engine.get_records(user_id)
    return UserObjectDetectionAgentResponse(
        user_id=user_id,
        object_detection_records=[
            ObjectDetectionRecordResponse.from_record(record) for record in records
        ],
    )


@object_detection_agent_router.get(
    "/object_detection_agent/{user_id}/{object_id}",
    response_model=ObjectDetectionRecordResponse,
    summary="Get one object detection record",
    description="Return one object detection record identified by object ID.",
)
async def get_object_detection_record(
    user_id: str,
    object_id: str,
) -> ObjectDetectionRecordResponse:
    """Return a single object detection record by ID."""
    decoded_id = parse_path_object_id(object_id)
    record = object_detection_agent_engine.get_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Object detection record not found",
        )

    return ObjectDetectionRecordResponse.from_record(record)


@object_detection_agent_router.put(
    "/object_detection_agent/{user_id}/{object_id}",
    response_model=ObjectDetectionRecordResponse,
    status_code=status.HTTP_200_OK,
    summary="Update object detection record",
    description="Replace an existing object detection record with updated data.",
)
async def update_object_detection_record(
    user_id: str,
    object_id: str,
    request: ObjectDetectionRecord,
) -> ObjectDetectionRecordResponse:
    """Update and return an object detection record."""
    decoded_id = parse_path_object_id(object_id)

    if normalize_object_id(request.object_id) != normalize_object_id(decoded_id):
        if object_detection_agent_engine.object_id_exists(user_id, request.object_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Object detection record already exists",
            )

    record = object_detection_agent_engine.update_record(
        user_id,
        decoded_id,
        request,
    )
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Object detection record not found",
        )

    return ObjectDetectionRecordResponse.from_record(record)


@object_detection_agent_router.delete(
    "/object_detection_agent/{user_id}/{object_id}",
    response_model=ObjectDetectionRecordResponse,
    summary="Delete object detection record",
    description="Delete an object detection record and return the removed record.",
)
async def delete_object_detection_record(
    user_id: str,
    object_id: str,
) -> ObjectDetectionRecordResponse:
    """Delete an object detection record and return the deleted item."""
    decoded_id = parse_path_object_id(object_id)
    record = object_detection_agent_engine.delete_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Object detection record not found",
        )

    return ObjectDetectionRecordResponse.from_record(record)
