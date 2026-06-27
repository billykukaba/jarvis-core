"""Pydantic schemas for the Emotion Recognition Agent."""

from pydantic import BaseModel, ConfigDict, Field


class EmotionRecognition(BaseModel):
    """Emotion recognition record stored for a user."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "emotion_id": "emotion_001",
                    "image_file": "portrait.jpg",
                    "detected_emotion": "happy",
                    "confidence_score": 89,
                    "status": "completed",
                    "progress_percentage": 100,
                    "created_at": "2026-06-04T09:00:00",
                    "updated_at": "2026-06-04T09:01:00",
                }
            ]
        }
    )

    emotion_id: str = Field(
        min_length=1,
        description="Unique emotion record identifier",
        examples=["emotion_001"],
    )
    image_file: str = Field(
        min_length=1,
        description="Image file name or path",
        examples=["portrait.jpg"],
    )
    detected_emotion: str = Field(
        min_length=1,
        description="Detected emotion label",
        examples=["happy"],
    )
    confidence_score: int = Field(
        ge=0,
        le=100,
        description="Emotion recognition confidence score",
        examples=[89],
    )
    status: str = Field(
        min_length=1,
        description="Current emotion recognition status",
        examples=["completed"],
    )
    progress_percentage: int = Field(
        ge=0,
        le=100,
        description="Recognition progress percentage",
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
        examples=["2026-06-04T09:01:00"],
    )


class EmotionRecognitionResponse(BaseModel):
    """Emotion recognition record returned by the API."""

    emotion_id: str
    image_file: str
    detected_emotion: str
    confidence_score: int
    status: str
    progress_percentage: int
    created_at: str
    updated_at: str

    @classmethod
    def from_emotion(
        cls,
        emotion: EmotionRecognition,
    ) -> "EmotionRecognitionResponse":
        """Build an API response from a stored emotion recognition record."""
        return cls(
            emotion_id=emotion.emotion_id,
            image_file=emotion.image_file,
            detected_emotion=emotion.detected_emotion,
            confidence_score=emotion.confidence_score,
            status=emotion.status,
            progress_percentage=emotion.progress_percentage,
            created_at=emotion.created_at,
            updated_at=emotion.updated_at,
        )


class UserEmotionRecognitionAgentResponse(BaseModel):
    """All emotion recognition records for one user."""

    user_id: str
    emotion_records: list[EmotionRecognitionResponse]
