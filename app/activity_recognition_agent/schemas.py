"""Pydantic schemas for the Activity Recognition Agent."""

from pydantic import BaseModel, ConfigDict, Field


class ActivityRecognition(BaseModel):
    """Activity recognition record stored for a user."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "activity_id": "activity_001",
                    "video_file": "gym_session.mp4",
                    "detected_activity": "running",
                    "confidence_score": 91,
                    "status": "completed",
                    "progress_percentage": 100,
                    "created_at": "2026-06-04T09:00:00",
                    "updated_at": "2026-06-04T09:04:00",
                }
            ]
        }
    )

    activity_id: str = Field(
        min_length=1,
        description="Unique activity record identifier",
        examples=["activity_001"],
    )
    video_file: str = Field(
        min_length=1,
        description="Video file name or path",
        examples=["gym_session.mp4"],
    )
    detected_activity: str = Field(
        min_length=1,
        description="Detected activity label",
        examples=["running"],
    )
    confidence_score: int = Field(
        ge=0,
        le=100,
        description="Activity recognition confidence score",
        examples=[91],
    )
    status: str = Field(
        min_length=1,
        description="Current activity recognition status",
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
        examples=["2026-06-04T09:04:00"],
    )


class ActivityRecognitionResponse(BaseModel):
    """Activity recognition record returned by the API."""

    activity_id: str
    video_file: str
    detected_activity: str
    confidence_score: int
    status: str
    progress_percentage: int
    created_at: str
    updated_at: str

    @classmethod
    def from_activity(
        cls,
        activity: ActivityRecognition,
    ) -> "ActivityRecognitionResponse":
        """Build an API response from a stored activity recognition record."""
        return cls(
            activity_id=activity.activity_id,
            video_file=activity.video_file,
            detected_activity=activity.detected_activity,
            confidence_score=activity.confidence_score,
            status=activity.status,
            progress_percentage=activity.progress_percentage,
            created_at=activity.created_at,
            updated_at=activity.updated_at,
        )


class UserActivityRecognitionAgentResponse(BaseModel):
    """All activity recognition records for one user."""

    user_id: str
    activity_records: list[ActivityRecognitionResponse]
