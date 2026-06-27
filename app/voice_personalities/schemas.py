"""Pydantic schemas for the Voice Personality Engine (Module 65)."""

from pydantic import BaseModel, ConfigDict, Field


class VoicePersonalityRecord(BaseModel):
    """Voice personality record stored for a user."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "personality": "Friendly Assistant",
                    "tone": "Warm",
                    "energy": "High",
                }
            ]
        }
    )

    personality: str = Field(
        min_length=1,
        description="Voice personality name",
        examples=["Friendly Assistant"],
    )
    tone: str = Field(
        min_length=1,
        description="Voice tone style",
        examples=["Warm"],
    )
    energy: str = Field(
        min_length=1,
        description="Voice energy level",
        examples=["High"],
    )


class VoicePersonalityRecordResponse(BaseModel):
    """Voice personality record returned by the API."""

    personality: str
    tone: str
    energy: str

    @classmethod
    def from_record(
        cls,
        record: VoicePersonalityRecord,
    ) -> "VoicePersonalityRecordResponse":
        """Build an API response from a stored voice personality record."""
        return cls(
            personality=record.personality,
            tone=record.tone,
            energy=record.energy,
        )


class UserVoicePersonalitiesResponse(BaseModel):
    """All voice personality records for one user."""

    user_id: str
    voice_personalities: list[VoicePersonalityRecordResponse]
