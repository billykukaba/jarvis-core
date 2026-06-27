"""Pydantic schemas for the Speech To Text Agent."""

from pydantic import BaseModel, ConfigDict, Field


class SpeechRecord(BaseModel):
    """Speech-to-text record stored for a user."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "speech_id": "speech_001",
                    "audio_file": "meeting_recording.wav",
                    "detected_language": "en-US",
                    "transcription": "Welcome to the quarterly review meeting.",
                    "confidence_score": 92,
                    "status": "completed",
                    "progress_percentage": 100,
                    "created_at": "2026-06-04T09:00:00",
                    "updated_at": "2026-06-04T09:05:00",
                }
            ]
        }
    )

    speech_id: str = Field(
        min_length=1,
        description="Unique speech record identifier",
        examples=["speech_001"],
    )
    audio_file: str = Field(
        min_length=1,
        description="Audio file name or path",
        examples=["meeting_recording.wav"],
    )
    detected_language: str = Field(
        min_length=1,
        description="Detected spoken language",
        examples=["en-US"],
    )
    transcription: str = Field(
        min_length=1,
        description="Transcribed text from the audio",
        examples=["Welcome to the quarterly review meeting."],
    )
    confidence_score: int = Field(
        ge=0,
        le=100,
        description="Transcription confidence score",
        examples=[92],
    )
    status: str = Field(
        min_length=1,
        description="Current transcription status",
        examples=["completed"],
    )
    progress_percentage: int = Field(
        ge=0,
        le=100,
        description="Transcription progress percentage",
        examples=[100],
    )
    created_at: str = Field(
        min_length=1,
        description="Record creation timestamp",
        examples=["2026-06-04T09:00:00"],
    )
    updated_at: str = Field(
        min_length=1,
        description="Record last update timestamp",
        examples=["2026-06-04T09:05:00"],
    )


class SpeechRecordResponse(BaseModel):
    """Speech record returned by the API."""

    speech_id: str
    audio_file: str
    detected_language: str
    transcription: str
    confidence_score: int
    status: str
    progress_percentage: int
    created_at: str
    updated_at: str

    @classmethod
    def from_record(cls, record: SpeechRecord) -> "SpeechRecordResponse":
        """Build an API response from a stored speech record."""
        return cls(
            speech_id=record.speech_id,
            audio_file=record.audio_file,
            detected_language=record.detected_language,
            transcription=record.transcription,
            confidence_score=record.confidence_score,
            status=record.status,
            progress_percentage=record.progress_percentage,
            created_at=record.created_at,
            updated_at=record.updated_at,
        )


class UserSpeechToTextAgentResponse(BaseModel):
    """All speech records for one user."""

    user_id: str
    speech_records: list[SpeechRecordResponse]
