"""FastAPI routes for the Autonomous Action Engine.

Plans, tracks and manages autonomous actions executed by Jarvis across tools,
systems and workflows.
"""

from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, status

from app.autonomous_action_engine.autonomous_action_engine_engine import (
    normalize_action_id,
)
from app.autonomous_action_engine.schemas import (
    AutonomousActionRecord,
    AutonomousActionRecordResponse,
    UserAutonomousActionEngineResponse,
)
from app.services.engine_registry import autonomous_action_engine

# Router exposed to FastAPI as autonomous_action_engine_router in main.py.
autonomous_action_engine_router = APIRouter(tags=["Autonomous Action Engine"])


def parse_path_action_id(action_id: str) -> str:
    """Decode URL path action IDs so spaces work in GET, PUT, and DELETE."""
    return unquote(action_id.replace("+", " "))


@autonomous_action_engine_router.post(
    "/autonomous_action_engine/{user_id}",
    response_model=AutonomousActionRecordResponse,
    summary="Create autonomous action",
    description=(
        "Create a new autonomous action record for the specified user. "
        "Plans, tracks and manages autonomous actions executed by Jarvis "
        "across tools, systems and workflows."
    ),
)
async def create_autonomous_action(
    user_id: str,
    request: AutonomousActionRecord,
) -> AutonomousActionRecordResponse:
    """Create and return an autonomous action record."""
    if autonomous_action_engine.action_id_exists(user_id, request.action_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Autonomous action already exists",
        )

    record = autonomous_action_engine.create_record(user_id, request)
    return AutonomousActionRecordResponse.from_record(record)


@autonomous_action_engine_router.get(
    "/autonomous_action_engine/{user_id}",
    response_model=UserAutonomousActionEngineResponse,
    summary="Get all autonomous actions",
    description=(
        "Return all autonomous action records saved by the specified user. "
        "Plans, tracks and manages autonomous actions executed by Jarvis "
        "across tools, systems and workflows."
    ),
)
async def get_autonomous_actions(
    user_id: str,
) -> UserAutonomousActionEngineResponse:
    """Return all autonomous action records for a user."""
    records = autonomous_action_engine.get_records(user_id)
    return UserAutonomousActionEngineResponse(
        user_id=user_id,
        autonomous_actions=[
            AutonomousActionRecordResponse.from_record(record)
            for record in records
        ],
    )


@autonomous_action_engine_router.get(
    "/autonomous_action_engine/{user_id}/{action_id}",
    response_model=AutonomousActionRecordResponse,
    summary="Get one autonomous action",
    description="Return one autonomous action record identified by action ID.",
)
async def get_autonomous_action(
    user_id: str,
    action_id: str,
) -> AutonomousActionRecordResponse:
    """Return a single autonomous action record by ID."""
    decoded_id = parse_path_action_id(action_id)
    record = autonomous_action_engine.get_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Autonomous action not found",
        )

    return AutonomousActionRecordResponse.from_record(record)


@autonomous_action_engine_router.put(
    "/autonomous_action_engine/{user_id}/{action_id}",
    response_model=AutonomousActionRecordResponse,
    status_code=status.HTTP_200_OK,
    summary="Update autonomous action",
    description="Replace an existing autonomous action record with updated data.",
)
async def update_autonomous_action(
    user_id: str,
    action_id: str,
    request: AutonomousActionRecord,
) -> AutonomousActionRecordResponse:
    """Update and return an autonomous action record."""
    decoded_id = parse_path_action_id(action_id)

    if normalize_action_id(request.action_id) != normalize_action_id(decoded_id):
        if autonomous_action_engine.action_id_exists(user_id, request.action_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Autonomous action already exists",
            )

    record = autonomous_action_engine.update_record(
        user_id,
        decoded_id,
        request,
    )
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Autonomous action not found",
        )

    return AutonomousActionRecordResponse.from_record(record)


@autonomous_action_engine_router.delete(
    "/autonomous_action_engine/{user_id}/{action_id}",
    response_model=AutonomousActionRecordResponse,
    summary="Delete autonomous action",
    description="Delete an autonomous action record and return the removed record.",
)
async def delete_autonomous_action(
    user_id: str,
    action_id: str,
) -> AutonomousActionRecordResponse:
    """Delete an autonomous action record and return the deleted item."""
    decoded_id = parse_path_action_id(action_id)
    record = autonomous_action_engine.delete_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Autonomous action not found",
        )

    return AutonomousActionRecordResponse.from_record(record)
