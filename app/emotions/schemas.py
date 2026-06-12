"""Pydantic schemas for the Emotion Service (Module 62)."""

from pydantic import BaseModel, ConfigDict, Field


class EmotionRecord(BaseModel):
    """Emotion record stored for a user."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "emotion": "Happy",
                    "intensity": "High",
                }
            ]
        }
    )

    emotion: str = Field(
        min_length=1,
        description="Emotion name",
        examples=["Happy"],
    )
    intensity: str = Field(
        min_length=1,
        description="Emotion intensity level",
        examples=["High"],
    )


class EmotionRecordResponse(BaseModel):
    """Emotion record returned by the API."""

    emotion: str
    intensity: str

    @classmethod
    def from_record(cls, record: EmotionRecord) -> "EmotionRecordResponse":
        """Build an API response from a stored emotion record."""
        return cls(
            emotion=record.emotion,
            intensity=record.intensity,
        )


class UserEmotionsResponse(BaseModel):
    """All emotion records for one user."""

    user_id: str
    emotions: list[EmotionRecordResponse]
