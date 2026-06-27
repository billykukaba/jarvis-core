"""Pydantic schemas for the Pose Estimation Agent."""

from pydantic import BaseModel, ConfigDict, Field


class PoseEstimation(BaseModel):
    """Pose estimation record stored for a user."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "pose_id": "pose_001",
                    "image_file": "yoga_pose.jpg",
                    "detected_pose": "warrior_ii",
                    "confidence_score": 88,
                    "status": "completed",
                    "progress_percentage": 100,
                    "created_at": "2026-06-04T09:00:00",
                    "updated_at": "2026-06-04T09:02:00",
                }
            ]
        }
    )

    pose_id: str = Field(
        min_length=1,
        description="Unique pose record identifier",
        examples=["pose_001"],
    )
    image_file: str = Field(
        min_length=1,
        description="Image file name or path",
        examples=["yoga_pose.jpg"],
    )
    detected_pose: str = Field(
        min_length=1,
        description="Detected pose label",
        examples=["warrior_ii"],
    )
    confidence_score: int = Field(
        ge=0,
        le=100,
        description="Pose estimation confidence score",
        examples=[88],
    )
    status: str = Field(
        min_length=1,
        description="Current pose estimation status",
        examples=["completed"],
    )
    progress_percentage: int = Field(
        ge=0,
        le=100,
        description="Estimation progress percentage",
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


class PoseEstimationResponse(BaseModel):
    """Pose estimation record returned by the API."""

    pose_id: str
    image_file: str
    detected_pose: str
    confidence_score: int
    status: str
    progress_percentage: int
    created_at: str
    updated_at: str

    @classmethod
    def from_pose(cls, pose: PoseEstimation) -> "PoseEstimationResponse":
        """Build an API response from a stored pose estimation record."""
        return cls(
            pose_id=pose.pose_id,
            image_file=pose.image_file,
            detected_pose=pose.detected_pose,
            confidence_score=pose.confidence_score,
            status=pose.status,
            progress_percentage=pose.progress_percentage,
            created_at=pose.created_at,
            updated_at=pose.updated_at,
        )


class UserPoseEstimationAgentResponse(BaseModel):
    """All pose estimation records for one user."""

    user_id: str
    pose_records: list[PoseEstimationResponse]
