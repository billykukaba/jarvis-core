"""Pydantic schemas for the Achievement Service."""

from pydantic import BaseModel, Field


class Achievement(BaseModel):
    """Achievement data stored for a user."""

    title: str = Field(min_length=1, description="Achievement title")
    description: str = Field(min_length=1, description="Achievement description")
    date: str = Field(min_length=1, description="Achievement date (YYYY-MM-DD)")
    level: str = Field(min_length=1, description="Achievement level or importance")


class AchievementResponse(BaseModel):
    """Achievement returned by the API."""

    title: str
    description: str
    date: str
    level: str

    @classmethod
    def from_achievement(cls, achievement: Achievement) -> "AchievementResponse":
        """Build an API response from a stored achievement."""
        return cls(
            title=achievement.title,
            description=achievement.description,
            date=achievement.date,
            level=achievement.level,
        )


class UserAchievementsResponse(BaseModel):
    """All achievements for one user."""

    user_id: str
    achievements: list[AchievementResponse]
