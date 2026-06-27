"""Pydantic schemas for the Goal Execution Agent."""

from pydantic import BaseModel, ConfigDict, Field


class GoalExecutionRecord(BaseModel):
    """Goal execution record stored for a user."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "goal_id": "goal_001",
                    "goal_name": "Launch MVP",
                    "goal_description": "Ship the minimum viable product to production",
                    "execution_steps": [
                        "Finalize scope",
                        "Implement core features",
                        "Deploy to production",
                    ],
                    "current_step": "Implement core features",
                    "completion_percentage": 45,
                    "priority_level": 1,
                    "status": "in_progress",
                    "created_at": "2026-06-04T09:00:00",
                    "updated_at": "2026-06-04T10:30:00",
                }
            ]
        }
    )

    goal_id: str = Field(
        min_length=1,
        description="Unique goal identifier",
        examples=["goal_001"],
    )
    goal_name: str = Field(
        min_length=1,
        description="Display name of the goal",
        examples=["Launch MVP"],
    )
    goal_description: str = Field(
        min_length=1,
        description="Detailed goal description",
        examples=["Ship the minimum viable product to production"],
    )
    execution_steps: list[str] = Field(
        min_length=1,
        description="Ordered list of execution steps",
        examples=[
            [
                "Finalize scope",
                "Implement core features",
                "Deploy to production",
            ]
        ],
    )
    current_step: str = Field(
        min_length=1,
        description="Step currently being executed",
        examples=["Implement core features"],
    )
    completion_percentage: int = Field(
        ge=0,
        le=100,
        description="Goal completion percentage",
        examples=[45],
    )
    priority_level: int = Field(
        ge=0,
        description="Goal priority level",
        examples=[1],
    )
    status: str = Field(
        min_length=1,
        description="Current goal execution status",
        examples=["in_progress"],
    )
    created_at: str = Field(
        min_length=1,
        description="Goal creation timestamp",
        examples=["2026-06-04T09:00:00"],
    )
    updated_at: str = Field(
        min_length=1,
        description="Goal last update timestamp",
        examples=["2026-06-04T10:30:00"],
    )


class GoalExecutionRecordResponse(BaseModel):
    """Goal execution record returned by the API."""

    goal_id: str
    goal_name: str
    goal_description: str
    execution_steps: list[str]
    current_step: str
    completion_percentage: int
    priority_level: int
    status: str
    created_at: str
    updated_at: str

    @classmethod
    def from_record(
        cls,
        record: GoalExecutionRecord,
    ) -> "GoalExecutionRecordResponse":
        """Build an API response from a stored goal execution record."""
        return cls(
            goal_id=record.goal_id,
            goal_name=record.goal_name,
            goal_description=record.goal_description,
            execution_steps=record.execution_steps,
            current_step=record.current_step,
            completion_percentage=record.completion_percentage,
            priority_level=record.priority_level,
            status=record.status,
            created_at=record.created_at,
            updated_at=record.updated_at,
        )


class UserGoalExecutionAgentResponse(BaseModel):
    """All goal execution records for one user."""

    user_id: str
    goals: list[GoalExecutionRecordResponse]
