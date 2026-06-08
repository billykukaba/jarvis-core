from fastapi import APIRouter, HTTPException, status

from app.goal_tracker.schemas import (
    GoalRequest,
    GoalResponse,
    ProgressUpdateRequest,
    UserGoalsResponse,
)
from app.services.engine_registry import goal_tracker_engine

router = APIRouter(tags=["goals-tracker"])


@router.post("/goals/{user_id}", response_model=GoalResponse)
async def add_goal(user_id: str, request: GoalRequest) -> GoalResponse:
    goal = goal_tracker_engine.add_goal(user_id, request.to_goal())
    return GoalResponse.from_goal(goal)


@router.get("/goals/{user_id}", response_model=UserGoalsResponse)
async def get_goals(user_id: str) -> UserGoalsResponse:
    goals = goal_tracker_engine.get_goals(user_id)
    return UserGoalsResponse(
        user_id=user_id,
        goals=[GoalResponse.from_goal(goal) for goal in goals],
    )


@router.get("/goals/{user_id}/{title}", response_model=GoalResponse)
async def get_goal(user_id: str, title: str) -> GoalResponse:
    goal = goal_tracker_engine.get_goal(user_id, title)
    if goal is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found",
        )

    return GoalResponse.from_goal(goal)


@router.post("/goals/{user_id}/{title}/progress", response_model=GoalResponse)
async def update_progress(
    user_id: str,
    title: str,
    request: ProgressUpdateRequest,
) -> GoalResponse:
    goal = goal_tracker_engine.update_progress(user_id, title, request.progress)
    if goal is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found",
        )

    return GoalResponse.from_goal(goal)


@router.post("/goals/{user_id}/{title}/complete", response_model=GoalResponse)
async def mark_completed(user_id: str, title: str) -> GoalResponse:
    goal = goal_tracker_engine.mark_completed(user_id, title)
    if goal is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found",
        )

    return GoalResponse.from_goal(goal)
