"""Pydantic schemas for the Habit Service."""

from pydantic import BaseModel, Field


class Habit(BaseModel):
    """Habit data stored for a user."""

    name: str = Field(min_length=1, description="Habit name")
    frequency: str = Field(min_length=1, description="How often the habit should be done")
    streak: int = Field(default=0, ge=0, description="Current streak count")
    completed_today: bool = Field(
        default=False,
        description="Whether the habit was completed today",
    )


class HabitResponse(BaseModel):
    """Habit returned by the API."""

    name: str
    frequency: str
    streak: int
    completed_today: bool

    @classmethod
    def from_habit(cls, habit: Habit) -> "HabitResponse":
        """Build an API response from a stored habit."""
        return cls(
            name=habit.name,
            frequency=habit.frequency,
            streak=habit.streak,
            completed_today=habit.completed_today,
        )


class UserHabitsResponse(BaseModel):
    """All habits for one user."""

    user_id: str
    habits: list[HabitResponse]
