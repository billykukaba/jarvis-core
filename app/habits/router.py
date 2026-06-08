"""FastAPI routes for the Habit Service."""

from fastapi import APIRouter, HTTPException, status

from app.habits.schemas import Habit, HabitResponse, UserHabitsResponse
from app.services.engine_registry import habit_service_engine

# Router exposed to FastAPI as habits_router in main.py.
habits_router = APIRouter(tags=["habits"])


@habits_router.post(
    "/habits/{user_id}",
    response_model=HabitResponse,
    summary="Create habit",
    description="Create a new habit for the specified user.",
)
async def create_habit(user_id: str, request: Habit) -> HabitResponse:
    """Create and return a habit."""
    habit = habit_service_engine.create_habit(user_id, request)
    return HabitResponse.from_habit(habit)


@habits_router.get(
    "/habits/{user_id}",
    response_model=UserHabitsResponse,
    summary="Get all habits",
    description="Return all habits saved by the specified user.",
)
async def get_habits(user_id: str) -> UserHabitsResponse:
    """Return all habits for a user."""
    habits = habit_service_engine.get_habits(user_id)
    return UserHabitsResponse(
        user_id=user_id,
        habits=[HabitResponse.from_habit(habit) for habit in habits],
    )


@habits_router.get(
    "/habits/{user_id}/{name}",
    response_model=HabitResponse,
    summary="Get one habit",
    description="Return one habit identified by its name.",
)
async def get_habit(user_id: str, name: str) -> HabitResponse:
    """Return a single habit by name."""
    habit = habit_service_engine.get_habit(user_id, name)
    if habit is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habit not found",
        )

    return HabitResponse.from_habit(habit)


@habits_router.put(
    "/habits/{user_id}/{name}",
    response_model=HabitResponse,
    summary="Update habit",
    description="Replace an existing habit with updated data.",
)
async def update_habit(user_id: str, name: str, request: Habit) -> HabitResponse:
    """Update and return a habit."""
    habit = habit_service_engine.update_habit(user_id, name, request)
    if habit is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habit not found",
        )

    return HabitResponse.from_habit(habit)


@habits_router.delete(
    "/habits/{user_id}/{name}",
    response_model=HabitResponse,
    summary="Delete habit",
    description="Delete a habit and return the removed habit.",
)
async def delete_habit(user_id: str, name: str) -> HabitResponse:
    """Delete a habit and return the deleted item."""
    habit = habit_service_engine.delete_habit(user_id, name)
    if habit is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habit not found",
        )

    return HabitResponse.from_habit(habit)
