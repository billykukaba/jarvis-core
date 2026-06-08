from pydantic import BaseModel, Field

from app.learning_tracker.learning_tracker_engine import LearningSkill


class LearningSkillRequest(BaseModel):
    skill_name: str = Field(min_length=1)
    level: str = Field(min_length=1)
    progress: int

    def to_skill(self) -> LearningSkill:
        return LearningSkill(
            skill_name=self.skill_name,
            level=self.level,
            progress=self.progress,
        )


class LearningProgressRequest(BaseModel):
    progress: int


class LearningSkillResponse(BaseModel):
    skill_name: str
    level: str
    progress: int

    @classmethod
    def from_skill(cls, skill: LearningSkill) -> "LearningSkillResponse":
        return cls(
            skill_name=skill.skill_name,
            level=skill.level,
            progress=skill.progress,
        )


class UserSkillsResponse(BaseModel):
    user_id: str
    skills: list[LearningSkillResponse]
