"""Pydantic schemas for the Avatar Animation Engine (Module 64)."""

from pydantic import BaseModel, ConfigDict, Field


class AvatarAnimationRecord(BaseModel):
    """Avatar animation record stored for a user."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "animation": "Wave",
                    "duration": "2 seconds",
                }
            ]
        }
    )

    animation: str = Field(
        min_length=1,
        description="Animation name",
        examples=["Wave"],
    )
    duration: str = Field(
        min_length=1,
        description="Animation duration",
        examples=["2 seconds"],
    )


class AvatarAnimationRecordResponse(BaseModel):
    """Avatar animation record returned by the API."""

    animation: str
    duration: str

    @classmethod
    def from_record(
        cls,
        record: AvatarAnimationRecord,
    ) -> "AvatarAnimationRecordResponse":
        """Build an API response from a stored avatar animation record."""
        return cls(
            animation=record.animation,
            duration=record.duration,
        )


class UserAvatarAnimationsResponse(BaseModel):
    """All avatar animation records for one user."""

    user_id: str
    avatar_animations: list[AvatarAnimationRecordResponse]
