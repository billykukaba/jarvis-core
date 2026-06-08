"""Pydantic schemas for the Goal Service."""

from typing import Literal

from pydantic import BaseModel, Field

GoalStatus = Literal["pending", "in_progress", "completed", "paused"]


class Goal(BaseModel):
    """Goal data stored for a user."""

    title: str = Field(min_length=1, description="Goal title")
    description: str = Field(min_length=1, description="Goal description")
    target_date: str = Field(min_length=1, description="Target date (YYYY-MM-DD)")
    status: GoalStatus = Field(
        default="in_progress",
        description="Goal status: pending, in_progress, completed, or paused",
    )


class GoalResponse(BaseModel):
    """Goal returned by the API."""

    title: str
    description: str
    target_date: str
    status: GoalStatus

    @classmethod
    def from_goal(cls, goal: Goal) -> "GoalResponse":
        """Build an API response from a stored goal."""
        return cls(
            title=goal.title,
            description=goal.description,
            target_date=goal.target_date,
            status=goal.status,
        )


class UserGoalsResponse(BaseModel):
    """All goals for one user."""

    user_id: str
    goals: list[GoalResponse]
