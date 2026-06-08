from fastapi import APIRouter, HTTPException, status

from app.models.goal import GoalRequest, GoalResponse
from app.services.engine_registry import goal_engine

router = APIRouter(tags=["goals"])


@router.post("/goals/{user_id}", response_model=GoalResponse)
async def create_goal(user_id: str, request: GoalRequest) -> GoalResponse:
    record = goal_engine.create_goal(user_id, request.title)
    return GoalResponse.from_record(record)


@router.get("/goals/{user_id}", response_model=list[GoalResponse])
async def get_goals(user_id: str) -> list[GoalResponse]:
    records = goal_engine.get_goals(user_id)
    return [GoalResponse.from_record(record) for record in records]


@router.post("/goals/{user_id}/{goal_id}/complete", response_model=GoalResponse)
async def complete_goal(user_id: str, goal_id: str) -> GoalResponse:
    record = goal_engine.complete_goal(user_id, goal_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found",
        )

    return GoalResponse.from_record(record)
