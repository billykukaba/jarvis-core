"""Pydantic schemas for the Learning Planner Engine (Module 58)."""

from pydantic import BaseModel, ConfigDict, Field


class LearningPlan(BaseModel):
    """Learning plan record stored for a user."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "plan_id": "plan_001",
                    "subject": "Python",
                    "goal": "Master FastAPI development",
                    "progress": 0,
                }
            ]
        }
    )

    plan_id: str = Field(
        min_length=1,
        description="Unique learning plan identifier",
        examples=["plan_001"],
    )
    subject: str = Field(
        min_length=1,
        description="Learning subject or topic",
        examples=["Python"],
    )
    goal: str = Field(
        min_length=1,
        description="Learning goal description",
        examples=["Master FastAPI development"],
    )
    progress: int = Field(
        ge=0,
        le=100,
        description="Learning progress percentage from 0 to 100",
        examples=[0],
    )


class LearningPlanResponse(BaseModel):
    """Learning plan record returned by the API."""

    plan_id: str
    subject: str
    goal: str
    progress: int

    @classmethod
    def from_plan(cls, plan: LearningPlan) -> "LearningPlanResponse":
        """Build an API response from a stored learning plan."""
        return cls(
            plan_id=plan.plan_id,
            subject=plan.subject,
            goal=plan.goal,
            progress=plan.progress,
        )


class UserLearningPlannerResponse(BaseModel):
    """All learning plans for one user."""

    user_id: str
    learning_plans: list[LearningPlanResponse]
