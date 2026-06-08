"""FastAPI routes for the Goal Service."""

from fastapi import APIRouter, HTTPException, status

from app.goals.schemas import Goal, GoalResponse, UserGoalsResponse
from app.services.engine_registry import goal_service_engine

# Router exposed to FastAPI as goals_router in main.py.
goals_router = APIRouter(tags=["goals"])


@goals_router.post(
    "/goals/{user_id}",
    response_model=GoalResponse,
    summary="Create goal",
    description="Create a new goal for the specified user.",
)
async def create_goal(user_id: str, request: Goal) -> GoalResponse:
    """Create and return a goal."""
    if goal_service_engine.title_exists(user_id, request.title):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Goal already exists",
        )

    goal = goal_service_engine.create_goal(user_id, request)
    return GoalResponse.from_goal(goal)


@goals_router.get(
    "/goals/{user_id}",
    response_model=UserGoalsResponse,
    summary="Get all goals",
    description="Return all goals saved by the specified user.",
)
async def get_goals(user_id: str) -> UserGoalsResponse:
    """Return all goals for a user."""
    goals = goal_service_engine.get_goals(user_id)
    return UserGoalsResponse(
        user_id=user_id,
        goals=[GoalResponse.from_goal(goal) for goal in goals],
    )


@goals_router.get(
    "/goals/{user_id}/{title}",
    response_model=GoalResponse,
    summary="Get one goal",
    description="Return one goal identified by its title.",
)
async def get_goal(user_id: str, title: str) -> GoalResponse:
    """Return a single goal by title."""
    goal = goal_service_engine.get_goal(user_id, title)
    if goal is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found",
        )

    return GoalResponse.from_goal(goal)


@goals_router.put(
    "/goals/{user_id}/{title}",
    response_model=GoalResponse,
    summary="Update goal",
    description="Replace an existing goal with updated data.",
)
async def update_goal(user_id: str, title: str, request: Goal) -> GoalResponse:
    """Update and return a goal."""
    if (
        request.title.lower() != title.lower()
        and goal_service_engine.title_exists(user_id, request.title)
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Goal already exists",
        )

    goal = goal_service_engine.update_goal(user_id, title, request)
    if goal is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found",
        )

    return GoalResponse.from_goal(goal)


@goals_router.delete(
    "/goals/{user_id}/{title}",
    response_model=GoalResponse,
    summary="Delete goal",
    description="Delete a goal and return the removed goal.",
)
async def delete_goal(user_id: str, title: str) -> GoalResponse:
    """Delete a goal and return the deleted item."""
    goal = goal_service_engine.delete_goal(user_id, title)
    if goal is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found",
        )

    return GoalResponse.from_goal(goal)
