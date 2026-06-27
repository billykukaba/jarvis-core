"""Pydantic schemas for the Vision Agent."""

from pydantic import BaseModel, ConfigDict, Field


class VisionRecord(BaseModel):
    """Vision analysis record stored for a user."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "image_id": "img_001",
                    "image_file": "office_scene.jpg",
                    "detected_objects": ["desk", "laptop", "chair", "person"],
                    "scene_description": "A person working at a desk in an office.",
                    "confidence_score": 88,
                    "status": "completed",
                    "progress_percentage": 100,
                    "created_at": "2026-06-04T09:00:00",
                    "updated_at": "2026-06-04T09:03:00",
                }
            ]
        }
    )

    image_id: str = Field(
        min_length=1,
        description="Unique vision record identifier",
        examples=["img_001"],
    )
    image_file: str = Field(
        min_length=1,
        description="Image file name or path",
        examples=["office_scene.jpg"],
    )
    detected_objects: list[str] = Field(
        min_length=1,
        description="Objects detected in the image",
        examples=[["desk", "laptop", "chair", "person"]],
    )
    scene_description: str = Field(
        min_length=1,
        description="Natural language description of the scene",
        examples=["A person working at a desk in an office."],
    )
    confidence_score: int = Field(
        ge=0,
        le=100,
        description="Vision analysis confidence score",
        examples=[88],
    )
    status: str = Field(
        min_length=1,
        description="Current vision analysis status",
        examples=["completed"],
    )
    progress_percentage: int = Field(
        ge=0,
        le=100,
        description="Vision analysis progress percentage",
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
        examples=["2026-06-04T09:03:00"],
    )


class VisionRecordResponse(BaseModel):
    """Vision record returned by the API."""

    image_id: str
    image_file: str
    detected_objects: list[str]
    scene_description: str
    confidence_score: int
    status: str
    progress_percentage: int
    created_at: str
    updated_at: str

    @classmethod
    def from_record(cls, record: VisionRecord) -> "VisionRecordResponse":
        """Build an API response from a stored vision record."""
        return cls(
            image_id=record.image_id,
            image_file=record.image_file,
            detected_objects=record.detected_objects,
            scene_description=record.scene_description,
            confidence_score=record.confidence_score,
            status=record.status,
            progress_percentage=record.progress_percentage,
            created_at=record.created_at,
            updated_at=record.updated_at,
        )


class UserVisionAgentResponse(BaseModel):
    """All vision records for one user."""

    user_id: str
    vision_records: list[VisionRecordResponse]
