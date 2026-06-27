"""FastAPI routes for the Activity Recognition Agent."""

from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, status

from app.activity_recognition_agent.activity_recognition_agent_engine import (
    normalize_activity_id,
)
from app.activity_recognition_agent.schemas import (
    ActivityRecognition,
    ActivityRecognitionResponse,
    UserActivityRecognitionAgentResponse,
)
from app.services.engine_registry import activity_recognition_agent_engine

# Router exposed to FastAPI as activity_recognition_agent_router in main.py.
activity_recognition_agent_router = APIRouter(tags=["Activity Recognition Agent"])


def parse_path_activity_id(activity_id: str) -> str:
    """Decode URL path activity IDs so spaces work in GET, PUT, and DELETE."""
    return unquote(activity_id.replace("+", " "))


@activity_recognition_agent_router.post(
    "/activity_recognition_agent/{user_id}",
    response_model=ActivityRecognitionResponse,
    summary="Create activity record",
    description="Create a new activity recognition record for the specified user.",
)
async def create_activity_record(
    user_id: str,
    request: ActivityRecognition,
) -> ActivityRecognitionResponse:
    """Create and return an activity recognition record."""
    if activity_recognition_agent_engine.activity_id_exists(
        user_id,
        request.activity_id,
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Activity record already exists",
        )

    record = activity_recognition_agent_engine.create_record(user_id, request)
    return ActivityRecognitionResponse.from_activity(record)


@activity_recognition_agent_router.get(
    "/activity_recognition_agent/{user_id}",
    response_model=UserActivityRecognitionAgentResponse,
    summary="Get all activity records",
    description="Return all activity recognition records saved by the specified user.",
)
async def get_activity_records(
    user_id: str,
) -> UserActivityRecognitionAgentResponse:
    """Return all activity recognition records for a user."""
    records = activity_recognition_agent_engine.get_records(user_id)
    return UserActivityRecognitionAgentResponse(
        user_id=user_id,
        activity_records=[
            ActivityRecognitionResponse.from_activity(record) for record in records
        ],
    )


@activity_recognition_agent_router.get(
    "/activity_recognition_agent/{user_id}/{activity_id}",
    response_model=ActivityRecognitionResponse,
    summary="Get one activity record",
    description="Return one activity recognition record identified by activity ID.",
)
async def get_activity_record(
    user_id: str,
    activity_id: str,
) -> ActivityRecognitionResponse:
    """Return a single activity recognition record by ID."""
    decoded_id = parse_path_activity_id(activity_id)
    record = activity_recognition_agent_engine.get_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity record not found",
        )

    return ActivityRecognitionResponse.from_activity(record)


@activity_recognition_agent_router.put(
    "/activity_recognition_agent/{user_id}/{activity_id}",
    response_model=ActivityRecognitionResponse,
    status_code=status.HTTP_200_OK,
    summary="Update activity record",
    description="Replace an existing activity recognition record with updated data.",
)
async def update_activity_record(
    user_id: str,
    activity_id: str,
    request: ActivityRecognition,
) -> ActivityRecognitionResponse:
    """Update and return an activity recognition record."""
    decoded_id = parse_path_activity_id(activity_id)

    if normalize_activity_id(request.activity_id) != normalize_activity_id(
        decoded_id
    ):
        if activity_recognition_agent_engine.activity_id_exists(
            user_id,
            request.activity_id,
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Activity record already exists",
            )

    record = activity_recognition_agent_engine.update_record(
        user_id,
        decoded_id,
        request,
    )
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity record not found",
        )

    return ActivityRecognitionResponse.from_activity(record)


@activity_recognition_agent_router.delete(
    "/activity_recognition_agent/{user_id}/{activity_id}",
    response_model=ActivityRecognitionResponse,
    summary="Delete activity record",
    description="Delete an activity recognition record and return the removed record.",
)
async def delete_activity_record(
    user_id: str,
    activity_id: str,
) -> ActivityRecognitionResponse:
    """Delete an activity recognition record and return the deleted item."""
    decoded_id = parse_path_activity_id(activity_id)
    record = activity_recognition_agent_engine.delete_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity record not found",
        )

    return ActivityRecognitionResponse.from_activity(record)
