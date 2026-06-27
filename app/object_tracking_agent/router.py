"""FastAPI routes for the Object Tracking Agent."""

from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, status

from app.object_tracking_agent.object_tracking_agent_engine import (
    normalize_tracking_id,
)
from app.object_tracking_agent.schemas import (
    ObjectTracking,
    ObjectTrackingResponse,
    UserObjectTrackingAgentResponse,
)
from app.services.engine_registry import object_tracking_agent_engine

# Router exposed to FastAPI as object_tracking_agent_router in main.py.
object_tracking_agent_router = APIRouter(tags=["Object Tracking Agent"])


def parse_path_tracking_id(tracking_id: str) -> str:
    """Decode URL path tracking IDs so spaces work in GET, PUT, and DELETE."""
    return unquote(tracking_id.replace("+", " "))


@object_tracking_agent_router.post(
    "/object_tracking_agent/{user_id}",
    response_model=ObjectTrackingResponse,
    summary="Create tracking record",
    description="Create a new object tracking record for the specified user.",
)
async def create_tracking_record(
    user_id: str,
    request: ObjectTracking,
) -> ObjectTrackingResponse:
    """Create and return an object tracking record."""
    if object_tracking_agent_engine.tracking_id_exists(user_id, request.tracking_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tracking record already exists",
        )

    record = object_tracking_agent_engine.create_record(user_id, request)
    return ObjectTrackingResponse.from_tracking(record)


@object_tracking_agent_router.get(
    "/object_tracking_agent/{user_id}",
    response_model=UserObjectTrackingAgentResponse,
    summary="Get all tracking records",
    description="Return all object tracking records saved by the specified user.",
)
async def get_tracking_records(
    user_id: str,
) -> UserObjectTrackingAgentResponse:
    """Return all object tracking records for a user."""
    records = object_tracking_agent_engine.get_records(user_id)
    return UserObjectTrackingAgentResponse(
        user_id=user_id,
        tracking_records=[
            ObjectTrackingResponse.from_tracking(record) for record in records
        ],
    )


@object_tracking_agent_router.get(
    "/object_tracking_agent/{user_id}/{tracking_id}",
    response_model=ObjectTrackingResponse,
    summary="Get one tracking record",
    description="Return one object tracking record identified by tracking ID.",
)
async def get_tracking_record(
    user_id: str,
    tracking_id: str,
) -> ObjectTrackingResponse:
    """Return a single object tracking record by ID."""
    decoded_id = parse_path_tracking_id(tracking_id)
    record = object_tracking_agent_engine.get_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tracking record not found",
        )

    return ObjectTrackingResponse.from_tracking(record)


@object_tracking_agent_router.put(
    "/object_tracking_agent/{user_id}/{tracking_id}",
    response_model=ObjectTrackingResponse,
    status_code=status.HTTP_200_OK,
    summary="Update tracking record",
    description="Replace an existing object tracking record with updated data.",
)
async def update_tracking_record(
    user_id: str,
    tracking_id: str,
    request: ObjectTracking,
) -> ObjectTrackingResponse:
    """Update and return an object tracking record."""
    decoded_id = parse_path_tracking_id(tracking_id)

    if normalize_tracking_id(request.tracking_id) != normalize_tracking_id(decoded_id):
        if object_tracking_agent_engine.tracking_id_exists(user_id, request.tracking_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tracking record already exists",
            )

    record = object_tracking_agent_engine.update_record(
        user_id,
        decoded_id,
        request,
    )
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tracking record not found",
        )

    return ObjectTrackingResponse.from_tracking(record)


@object_tracking_agent_router.delete(
    "/object_tracking_agent/{user_id}/{tracking_id}",
    response_model=ObjectTrackingResponse,
    summary="Delete tracking record",
    description="Delete an object tracking record and return the removed record.",
)
async def delete_tracking_record(
    user_id: str,
    tracking_id: str,
) -> ObjectTrackingResponse:
    """Delete an object tracking record and return the deleted item."""
    decoded_id = parse_path_tracking_id(tracking_id)
    record = object_tracking_agent_engine.delete_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tracking record not found",
        )

    return ObjectTrackingResponse.from_tracking(record)
