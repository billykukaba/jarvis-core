"""Pydantic schemas for the Camera Analysis Agent."""

from pydantic import BaseModel, ConfigDict, Field


class CameraAnalysisRecord(BaseModel):
    """Camera analysis record stored for a user."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "camera_id": "camera_001",
                    "camera_file": "living_room_feed.mp4",
                    "detected_scene": "indoor_living_room",
                    "detected_objects": ["sofa", "lamp", "person", "coffee_table"],
                    "camera_summary": "Living room scene with one person seated on the sofa.",
                    "confidence_score": 88,
                    "status": "completed",
                    "progress_percentage": 100,
                    "created_at": "2026-06-04T10:00:00",
                    "updated_at": "2026-06-04T10:03:00",
                }
            ]
        }
    )

    camera_id: str = Field(
        min_length=1,
        description="Unique camera analysis record identifier",
        examples=["camera_001"],
    )
    camera_file: str = Field(
        min_length=1,
        description="Camera feed file name or path",
        examples=["living_room_feed.mp4"],
    )
    detected_scene: str = Field(
        min_length=1,
        description="Scene classification detected from the camera feed",
        examples=["indoor_living_room"],
    )
    detected_objects: list[str] = Field(
        min_length=1,
        description="Objects detected in the camera feed",
        examples=[["sofa", "lamp", "person", "coffee_table"]],
    )
    camera_summary: str = Field(
        min_length=1,
        description="Natural language summary of the camera feed content",
        examples=["Living room scene with one person seated on the sofa."],
    )
    confidence_score: int = Field(
        ge=0,
        le=100,
        description="Camera analysis confidence score",
        examples=[88],
    )
    status: str = Field(
        min_length=1,
        description="Current camera analysis status",
        examples=["completed"],
    )
    progress_percentage: int = Field(
        ge=0,
        le=100,
        description="Camera analysis progress percentage",
        examples=[100],
    )
    created_at: str = Field(
        min_length=1,
        description="Record creation timestamp",
        examples=["2026-06-04T10:00:00"],
    )
    updated_at: str = Field(
        min_length=1,
        description="Record last update timestamp",
        examples=["2026-06-04T10:03:00"],
    )


class CameraAnalysisRecordResponse(BaseModel):
    """Camera analysis record returned by the API."""

    camera_id: str
    camera_file: str
    detected_scene: str
    detected_objects: list[str]
    camera_summary: str
    confidence_score: int
    status: str
    progress_percentage: int
    created_at: str
    updated_at: str

    @classmethod
    def from_record(
        cls,
        record: CameraAnalysisRecord,
    ) -> "CameraAnalysisRecordResponse":
        """Build an API response from a stored camera analysis record."""
        return cls(
            camera_id=record.camera_id,
            camera_file=record.camera_file,
            detected_scene=record.detected_scene,
            detected_objects=record.detected_objects,
            camera_summary=record.camera_summary,
            confidence_score=record.confidence_score,
            status=record.status,
            progress_percentage=record.progress_percentage,
            created_at=record.created_at,
            updated_at=record.updated_at,
        )


class UserCameraAnalysisAgentResponse(BaseModel):
    """All camera analysis records for one user."""

    user_id: str
    camera_analysis_records: list[CameraAnalysisRecordResponse]
