"""Pydantic schemas for the Text To Speech Agent."""

from pydantic import BaseModel, ConfigDict, Field


class TextToSpeechRecord(BaseModel):
    """Text-to-speech record stored for a user."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "tts_id": "tts_001",
                    "input_text": "Welcome to the quarterly review meeting.",
                    "output_audio_file": "welcome_message.mp3",
                    "language": "en-US",
                    "voice_name": "Aria",
                    "status": "completed",
                    "progress_percentage": 100,
                    "created_at": "2026-06-04T09:00:00",
                    "updated_at": "2026-06-04T09:02:00",
                }
            ]
        }
    )

    tts_id: str = Field(
        min_length=1,
        description="Unique text-to-speech record identifier",
        examples=["tts_001"],
    )
    input_text: str = Field(
        min_length=1,
        description="Text to convert to speech",
        examples=["Welcome to the quarterly review meeting."],
    )
    output_audio_file: str = Field(
        min_length=1,
        description="Generated audio file name or path",
        examples=["welcome_message.mp3"],
    )
    language: str = Field(
        min_length=1,
        description="Target spoken language",
        examples=["en-US"],
    )
    voice_name: str = Field(
        min_length=1,
        description="Voice profile used for synthesis",
        examples=["Aria"],
    )
    status: str = Field(
        min_length=1,
        description="Current synthesis status",
        examples=["completed"],
    )
    progress_percentage: int = Field(
        ge=0,
        le=100,
        description="Synthesis progress percentage",
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
        examples=["2026-06-04T09:02:00"],
    )


class TextToSpeechRecordResponse(BaseModel):
    """Text-to-speech record returned by the API."""

    tts_id: str
    input_text: str
    output_audio_file: str
    language: str
    voice_name: str
    status: str
    progress_percentage: int
    created_at: str
    updated_at: str

    @classmethod
    def from_record(cls, record: TextToSpeechRecord) -> "TextToSpeechRecordResponse":
        """Build an API response from a stored TTS record."""
        return cls(
            tts_id=record.tts_id,
            input_text=record.input_text,
            output_audio_file=record.output_audio_file,
            language=record.language,
            voice_name=record.voice_name,
            status=record.status,
            progress_percentage=record.progress_percentage,
            created_at=record.created_at,
            updated_at=record.updated_at,
        )


class UserTextToSpeechAgentResponse(BaseModel):
    """All text-to-speech records for one user."""

    user_id: str
    tts_records: list[TextToSpeechRecordResponse]
