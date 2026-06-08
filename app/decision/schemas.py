from pydantic import BaseModel, Field

from app.decision.decision_engine import DecisionResult


class DecisionRequest(BaseModel):
    question: str = Field(min_length=1)


class DecisionResponse(BaseModel):
    decision: str
    reason: str

    @classmethod
    def from_result(cls, result: DecisionResult) -> "DecisionResponse":
        return cls(
            decision=result.decision,
            reason=result.reason,
        )
