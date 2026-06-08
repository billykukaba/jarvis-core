"""Pydantic schemas for the Skills Service."""

from pydantic import BaseModel, Field


class Skill(BaseModel):
    """Skill record stored for a user."""

    skill: str = Field(min_length=1, description="Skill name")
    level: str = Field(min_length=1, description="Proficiency level (e.g. Beginner, Advanced)")


class SkillResponse(BaseModel):
    """Skill record returned by the API."""

    skill: str
    level: str

    @classmethod
    def from_skill(cls, skill: Skill) -> "SkillResponse":
        """Build an API response from a stored skill record."""
        return cls(
            skill=skill.skill,
            level=skill.level,
        )


class UserSkillsResponse(BaseModel):
    """All skill records for one user."""

    user_id: str
    skills: list[SkillResponse]
