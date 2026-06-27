"""FastAPI routes for the Learning Planner Engine (Module 58)."""

from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, status

from app.learning_planner.learning_planner_engine import normalize_plan_id
from app.learning_planner.schemas import (
    LearningPlan,
    LearningPlanResponse,
    UserLearningPlannerResponse,
)
from app.services.engine_registry import learning_planner_engine

# Router exposed to FastAPI as learning_planner_router in main.py.
learning_planner_router = APIRouter(tags=["Learning Planner Engine"])


def parse_path_plan_id(plan_id: str) -> str:
    """Decode URL path plan IDs so spaces work in GET, PUT, and DELETE."""
    return unquote(plan_id.replace("+", " "))


@learning_planner_router.post(
    "/learning_planner/{user_id}",
    response_model=LearningPlanResponse,
    summary="Create learning plan",
    description="Create a new learning plan for the specified user.",
)
async def create_learning_plan(
    user_id: str,
    request: LearningPlan,
) -> LearningPlanResponse:
    """Create and return a learning plan."""
    if learning_planner_engine.plan_id_exists(user_id, request.plan_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Plan already exists",
        )

    record = learning_planner_engine.create_record(user_id, request)
    return LearningPlanResponse.from_plan(record)


@learning_planner_router.get(
    "/learning_planner/{user_id}",
    response_model=UserLearningPlannerResponse,
    summary="Get all learning plans",
    description="Return all learning plans saved by the specified user.",
)
async def get_learning_plans(user_id: str) -> UserLearningPlannerResponse:
    """Return all learning plans for a user."""
    records = learning_planner_engine.get_records(user_id)
    return UserLearningPlannerResponse(
        user_id=user_id,
        learning_plans=[
            LearningPlanResponse.from_plan(record) for record in records
        ],
    )


@learning_planner_router.get(
    "/learning_planner/{user_id}/{plan_id}",
    response_model=LearningPlanResponse,
    summary="Get one learning plan",
    description="Return one learning plan identified by plan ID.",
)
async def get_learning_plan(
    user_id: str,
    plan_id: str,
) -> LearningPlanResponse:
    """Return a single learning plan by ID."""
    decoded_id = parse_path_plan_id(plan_id)
    record = learning_planner_engine.get_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plan not found",
        )

    return LearningPlanResponse.from_plan(record)


@learning_planner_router.put(
    "/learning_planner/{user_id}/{plan_id}",
    response_model=LearningPlanResponse,
    status_code=status.HTTP_200_OK,
    summary="Update learning plan",
    description="Replace an existing learning plan with updated data.",
)
async def update_learning_plan(
    user_id: str,
    plan_id: str,
    request: LearningPlan,
) -> LearningPlanResponse:
    """Update and return a learning plan."""
    decoded_id = parse_path_plan_id(plan_id)

    # Allow keeping the same plan ID while changing subject/goal/progress.
    if normalize_plan_id(request.plan_id) != normalize_plan_id(decoded_id):
        if learning_planner_engine.plan_id_exists(user_id, request.plan_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Plan already exists",
            )

    record = learning_planner_engine.update_record(user_id, decoded_id, request)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plan not found",
        )

    return LearningPlanResponse.from_plan(record)


@learning_planner_router.delete(
    "/learning_planner/{user_id}/{plan_id}",
    response_model=LearningPlanResponse,
    summary="Delete learning plan",
    description="Delete a learning plan and return the removed record.",
)
async def delete_learning_plan(
    user_id: str,
    plan_id: str,
) -> LearningPlanResponse:
    """Delete a learning plan and return the deleted item."""
    decoded_id = parse_path_plan_id(plan_id)
    record = learning_planner_engine.delete_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plan not found",
        )

    return LearningPlanResponse.from_plan(record)
