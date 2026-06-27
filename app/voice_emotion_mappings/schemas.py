"""Pydantic schemas for the Voice Emotion Mapping Engine (Module 66)."""

from pydantic import BaseModel, ConfigDict, Field


class VoiceEmotionMappingRecord(BaseModel):
    """Voice emotion mapping record stored for a user."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "emotion": "Happy",
                    "voice_style": "Cheerful",
                    "speech_speed": "Normal",
                }
            ]
        }
    )

    emotion: str = Field(
        min_length=1,
        description="Emotion name",
        examples=["Happy"],
    )
    voice_style: str = Field(
        min_length=1,
        description="Voice style for the emotion",
        examples=["Cheerful"],
    )
    speech_speed: str = Field(
        min_length=1,
        description="Speech speed for the emotion",
        examples=["Normal"],
    )


class VoiceEmotionMappingRecordResponse(BaseModel):
    """Voice emotion mapping record returned by the API."""

    emotion: str
    voice_style: str
    speech_speed: str

    @classmethod
    def from_record(
        cls,
        record: VoiceEmotionMappingRecord,
    ) -> "VoiceEmotionMappingRecordResponse":
        """Build an API response from a stored voice emotion mapping record."""
        return cls(
            emotion=record.emotion,
            voice_style=record.voice_style,
            speech_speed=record.speech_speed,
        )


class UserVoiceEmotionMappingsResponse(BaseModel):
    """All voice emotion mapping records for one user."""

    user_id: str
    voice_emotion_mappings: list[VoiceEmotionMappingRecordResponse]
