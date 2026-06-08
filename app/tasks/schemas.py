"""Pydantic schemas for the Task Service."""

from typing import Literal

from pydantic import BaseModel, Field

TaskStatus = Literal["pending", "in_progress", "completed"]


class Task(BaseModel):
    """Task data stored for a user."""

    title: str = Field(min_length=1, description="Task title")
    description: str = Field(min_length=1, description="Task description")
    status: TaskStatus = Field(
        default="pending",
        description="Task status: pending, in_progress, or completed",
    )


class TaskResponse(BaseModel):
    """Task returned by the API."""

    title: str
    description: str
    status: TaskStatus

    @classmethod
    def from_task(cls, task: Task) -> "TaskResponse":
        """Build an API response from a stored task."""
        return cls(
            title=task.title,
            description=task.description,
            status=task.status,
        )


class UserTasksResponse(BaseModel):
    """All tasks for one user."""

    user_id: str
    tasks: list[TaskResponse]
