"""FastAPI routes for the User Timeline Engine.

Tracks important user events, milestones, project progress, goals and personal
history for Jarvis chronological memory.
"""

from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, status

from app.user_timeline_engine.schemas import (
    UserTimelineEngineResponse,
    UserTimelineRecord,
    UserTimelineRecordResponse,
)
from app.user_timeline_engine.user_timeline_engine_engine import normalize_timeline_id
from app.services.engine_registry import user_timeline_engine

# Router exposed to FastAPI as user_timeline_engine_router in main.py.
user_timeline_engine_router = APIRouter(tags=["User Timeline Engine"])


def parse_path_timeline_id(timeline_id: str) -> str:
    """Decode URL path timeline IDs so spaces work in GET, PUT, and DELETE."""
    return unquote(timeline_id.replace("+", " "))


@user_timeline_engine_router.post(
    "/user_timeline_engine/{user_id}",
    response_model=UserTimelineRecordResponse,
    summary="Create timeline record",
    description=(
        "Create a new user timeline record for the specified user. "
        "Tracks important user events, milestones, project progress, goals "
        "and personal history for Jarvis chronological memory."
    ),
)
async def create_user_timeline_record(
    user_id: str,
    request: UserTimelineRecord,
) -> UserTimelineRecordResponse:
    """Create and return a user timeline record."""
    if user_timeline_engine.timeline_id_exists(user_id, request.timeline_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Timeline record already exists",
        )

    record = user_timeline_engine.create_record(user_id, request)
    return UserTimelineRecordResponse.from_record(record)


@user_timeline_engine_router.get(
    "/user_timeline_engine/{user_id}",
    response_model=UserTimelineEngineResponse,
    summary="Get all timeline records",
    description=(
        "Return all user timeline records saved by the specified user. "
        "Tracks important user events, milestones, project progress, goals "
        "and personal history for Jarvis chronological memory."
    ),
)
async def get_user_timeline_records(
    user_id: str,
) -> UserTimelineEngineResponse:
    """Return all user timeline records for a user."""
    records = user_timeline_engine.get_records(user_id)
    return UserTimelineEngineResponse(
        user_id=user_id,
        timeline_records=[
            UserTimelineRecordResponse.from_record(record) for record in records
        ],
    )


@user_timeline_engine_router.get(
    "/user_timeline_engine/{user_id}/{timeline_id}",
    response_model=UserTimelineRecordResponse,
    summary="Get one timeline record",
    description="Return one user timeline record identified by timeline ID.",
)
async def get_user_timeline_record(
    user_id: str,
    timeline_id: str,
) -> UserTimelineRecordResponse:
    """Return a single user timeline record by ID."""
    decoded_id = parse_path_timeline_id(timeline_id)
    record = user_timeline_engine.get_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Timeline record not found",
        )

    return UserTimelineRecordResponse.from_record(record)


@user_timeline_engine_router.put(
    "/user_timeline_engine/{user_id}/{timeline_id}",
    response_model=UserTimelineRecordResponse,
    status_code=status.HTTP_200_OK,
    summary="Update timeline record",
    description="Replace an existing user timeline record with updated data.",
)
async def update_user_timeline_record(
    user_id: str,
    timeline_id: str,
    request: UserTimelineRecord,
) -> UserTimelineRecordResponse:
    """Update and return a user timeline record."""
    decoded_id = parse_path_timeline_id(timeline_id)

    if normalize_timeline_id(request.timeline_id) != normalize_timeline_id(decoded_id):
        if user_timeline_engine.timeline_id_exists(user_id, request.timeline_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Timeline record already exists",
            )

    record = user_timeline_engine.update_record(
        user_id,
        decoded_id,
        request,
    )
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Timeline record not found",
        )

    return UserTimelineRecordResponse.from_record(record)


@user_timeline_engine_router.delete(
    "/user_timeline_engine/{user_id}/{timeline_id}",
    response_model=UserTimelineRecordResponse,
    summary="Delete timeline record",
    description="Delete a user timeline record and return the removed record.",
)
async def delete_user_timeline_record(
    user_id: str,
    timeline_id: str,
) -> UserTimelineRecordResponse:
    """Delete a user timeline record and return the deleted item."""
    decoded_id = parse_path_timeline_id(timeline_id)
    record = user_timeline_engine.delete_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Timeline record not found",
        )

    return UserTimelineRecordResponse.from_record(record)
