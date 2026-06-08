from datetime import datetime

from pydantic import BaseModel, Field

from app.consciousness.goal_engine import GoalRecord


class GoalRequest(BaseModel):
    title: str = Field(min_length=1)


class GoalResponse(BaseModel):
    id: str
    title: str
    completed: bool
    created_at: datetime

    @classmethod
    def from_record(cls, record: GoalRecord) -> "GoalResponse":
        return cls(
            id=record.id,
            title=record.title,
            completed=record.completed,
            created_at=record.created_at,
        )
