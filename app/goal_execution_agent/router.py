"""FastAPI routes for the Goal Execution Agent."""

from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, status

from app.goal_execution_agent.goal_execution_agent_engine import normalize_goal_id
from app.goal_execution_agent.schemas import (
    GoalExecutionRecord,
    GoalExecutionRecordResponse,
    UserGoalExecutionAgentResponse,
)
from app.services.engine_registry import goal_execution_agent_engine

# Router exposed to FastAPI as goal_execution_agent_router in main.py.
goal_execution_agent_router = APIRouter(tags=["Goal Execution Agent"])


def parse_path_goal_id(goal_id: str) -> str:
    """Decode URL path goal IDs so spaces work in GET, PUT, and DELETE."""
    return unquote(goal_id.replace("+", " "))


@goal_execution_agent_router.post(
    "/goal_execution_agent/{user_id}",
    response_model=GoalExecutionRecordResponse,
    summary="Create goal",
    description="Create a new goal execution record for the specified user.",
)
async def create_goal_execution_record(
    user_id: str,
    request: GoalExecutionRecord,
) -> GoalExecutionRecordResponse:
    """Create and return a goal execution record."""
    if goal_execution_agent_engine.goal_id_exists(user_id, request.goal_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Goal already exists",
        )

    record = goal_execution_agent_engine.create_record(user_id, request)
    return GoalExecutionRecordResponse.from_record(record)


@goal_execution_agent_router.get(
    "/goal_execution_agent/{user_id}",
    response_model=UserGoalExecutionAgentResponse,
    summary="Get all goals",
    description="Return all goal execution records saved by the specified user.",
)
async def get_goal_execution_records(
    user_id: str,
) -> UserGoalExecutionAgentResponse:
    """Return all goal execution records for a user."""
    records = goal_execution_agent_engine.get_records(user_id)
    return UserGoalExecutionAgentResponse(
        user_id=user_id,
        goals=[
            GoalExecutionRecordResponse.from_record(record) for record in records
        ],
    )


@goal_execution_agent_router.get(
    "/goal_execution_agent/{user_id}/{goal_id}",
    response_model=GoalExecutionRecordResponse,
    summary="Get one goal",
    description="Return one goal execution record identified by goal ID.",
)
async def get_goal_execution_record(
    user_id: str,
    goal_id: str,
) -> GoalExecutionRecordResponse:
    """Return a single goal execution record by ID."""
    decoded_id = parse_path_goal_id(goal_id)
    record = goal_execution_agent_engine.get_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found",
        )

    return GoalExecutionRecordResponse.from_record(record)


@goal_execution_agent_router.put(
    "/goal_execution_agent/{user_id}/{goal_id}",
    response_model=GoalExecutionRecordResponse,
    status_code=status.HTTP_200_OK,
    summary="Update goal",
    description="Replace an existing goal execution record with updated data.",
)
async def update_goal_execution_record(
    user_id: str,
    goal_id: str,
    request: GoalExecutionRecord,
) -> GoalExecutionRecordResponse:
    """Update and return a goal execution record."""
    decoded_id = parse_path_goal_id(goal_id)

    if normalize_goal_id(request.goal_id) != normalize_goal_id(decoded_id):
        if goal_execution_agent_engine.goal_id_exists(user_id, request.goal_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Goal already exists",
            )

    record = goal_execution_agent_engine.update_record(user_id, decoded_id, request)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found",
        )

    return GoalExecutionRecordResponse.from_record(record)


@goal_execution_agent_router.delete(
    "/goal_execution_agent/{user_id}/{goal_id}",
    response_model=GoalExecutionRecordResponse,
    summary="Delete goal",
    description="Delete a goal execution record and return the removed record.",
)
async def delete_goal_execution_record(
    user_id: str,
    goal_id: str,
) -> GoalExecutionRecordResponse:
    """Delete a goal execution record and return the deleted item."""
    decoded_id = parse_path_goal_id(goal_id)
    record = goal_execution_agent_engine.delete_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found",
        )

    return GoalExecutionRecordResponse.from_record(record)
