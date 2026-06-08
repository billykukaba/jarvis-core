from fastapi import APIRouter, HTTPException, status

from app.planning.schemas import PlanRequest, PlanResponse, UserPlansResponse
from app.services.engine_registry import planning_engine

router = APIRouter(tags=["planning"])


@router.post("/planning/{user_id}", response_model=PlanResponse)
async def create_plan(user_id: str, request: PlanRequest) -> PlanResponse:
    plan = planning_engine.create_plan(
        user_id=user_id,
        objective=request.objective,
        steps=request.steps,
    )
    return PlanResponse.from_plan(plan)


@router.get("/planning/{user_id}", response_model=UserPlansResponse)
async def get_plans(user_id: str) -> UserPlansResponse:
    plans = planning_engine.get_plans(user_id)
    return UserPlansResponse(
        user_id=user_id,
        plans=[PlanResponse.from_plan(plan) for plan in plans],
    )


@router.get("/planning/{user_id}/{objective}", response_model=PlanResponse)
async def get_plan(user_id: str, objective: str) -> PlanResponse:
    plan = planning_engine.get_plan(user_id, objective)
    if plan is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plan not found",
        )

    return PlanResponse.from_plan(plan)
