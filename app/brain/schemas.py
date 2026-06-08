from pydantic import BaseModel, Field

from app.brain.brain_engine import BrainResult
from app.profile.schemas import ProfileResponse


class BrainRequest(BaseModel):
    message: str = Field(min_length=1)


class BrainResponse(BaseModel):
    profile: ProfileResponse
    reasoning: str
    decision: str
    plan: list[str]
    recommended_skills: list[str]

    @classmethod
    def from_result(cls, result: BrainResult) -> "BrainResponse":
        return cls(
            profile=ProfileResponse.from_profile(result.profile),
            reasoning=result.reasoning,
            decision=result.decision,
            plan=result.plan,
            recommended_skills=result.recommended_skills,
        )
