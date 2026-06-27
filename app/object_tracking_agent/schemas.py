"""Pydantic schemas for the Object Tracking Agent."""

from pydantic import BaseModel, ConfigDict, Field


class ObjectTracking(BaseModel):
    """Object tracking record stored for a user."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "tracking_id": "track_001",
                    "video_file": "warehouse_feed.mp4",
                    "tracked_object": "forklift",
                    "tracking_status": "active",
                    "confidence_score": 87,
                    "status": "in_progress",
                    "progress_percentage": 65,
                    "created_at": "2026-06-04T09:00:00",
                    "updated_at": "2026-06-04T09:05:00",
                }
            ]
        }
    )

    tracking_id: str = Field(
        min_length=1,
        description="Unique object tracking record identifier",
        examples=["track_001"],
    )
    video_file: str = Field(
        min_length=1,
        description="Video file name or path",
        examples=["warehouse_feed.mp4"],
    )
    tracked_object: str = Field(
        min_length=1,
        description="Object being tracked in the video",
        examples=["forklift"],
    )
    tracking_status: str = Field(
        min_length=1,
        description="Current tracking state",
        examples=["active"],
    )
    confidence_score: int = Field(
        ge=0,
        le=100,
        description="Object tracking confidence score",
        examples=[87],
    )
    status: str = Field(
        min_length=1,
        description="Processing status of the tracking job",
        examples=["in_progress"],
    )
    progress_percentage: int = Field(
        ge=0,
        le=100,
        description="Tracking progress percentage",
        examples=[65],
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


class ObjectTrackingResponse(BaseModel):
    """Object tracking record returned by the API."""

    tracking_id: str
    video_file: str
    tracked_object: str
    tracking_status: str
    confidence_score: int
    status: str
    progress_percentage: int
    created_at: str
    updated_at: str

    @classmethod
    def from_tracking(cls, tracking: ObjectTracking) -> "ObjectTrackingResponse":
        """Build an API response from a stored object tracking record."""
        return cls(
            tracking_id=tracking.tracking_id,
            video_file=tracking.video_file,
            tracked_object=tracking.tracked_object,
            tracking_status=tracking.tracking_status,
            confidence_score=tracking.confidence_score,
            status=tracking.status,
            progress_percentage=tracking.progress_percentage,
            created_at=tracking.created_at,
            updated_at=tracking.updated_at,
        )


class UserObjectTrackingAgentResponse(BaseModel):
    """All object tracking records for one user."""

    user_id: str
    tracking_records: list[ObjectTrackingResponse]
