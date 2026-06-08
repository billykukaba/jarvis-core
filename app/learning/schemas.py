from pydantic import BaseModel, Field

from app.learning.learning_engine import LearnedSkill


class LearningRequest(BaseModel):
    skill: str = Field(min_length=1)


class LearningResponse(BaseModel):
    user_id: str
    learned_skill: str
    status: str

    @classmethod
    def from_skill(cls, skill: LearnedSkill) -> "LearningResponse":
        return cls(
            user_id=skill.user_id,
            learned_skill=skill.learned_skill,
            status=skill.status,
        )


class UserSkillsResponse(BaseModel):
    user_id: str
    skills: list[str]
