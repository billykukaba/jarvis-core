from pydantic import BaseModel, Field

from app.planning.planning_engine import Plan


class PlanRequest(BaseModel):
    objective: str = Field(min_length=1)
    steps: list[str]


class PlanResponse(BaseModel):
    objective: str
    steps: list[str]

    @classmethod
    def from_plan(cls, plan: Plan) -> "PlanResponse":
        return cls(
            objective=plan.objective,
            steps=plan.steps,
        )


class UserPlansResponse(BaseModel):
    user_id: str
    plans: list[PlanResponse]
