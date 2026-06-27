"""Pydantic schemas for the Image Understanding Agent."""

from pydantic import BaseModel, ConfigDict, Field


class ImageUnderstandingRecord(BaseModel):
    """Image understanding record stored for a user."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "image_id": "img_001",
                    "image_file": "street_scene.jpg",
                    "scene_description": "A busy urban street with pedestrians and cars.",
                    "detected_objects": ["person", "car", "traffic_light", "building"],
                    "confidence_score": 90,
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
        description="Unique image understanding record identifier",
        examples=["img_001"],
    )
    image_file: str = Field(
        min_length=1,
        description="Image file name or path",
        examples=["street_scene.jpg"],
    )
    scene_description: str = Field(
        min_length=1,
        description="Natural language description of the scene",
        examples=["A busy urban street with pedestrians and cars."],
    )
    detected_objects: list[str] = Field(
        min_length=1,
        description="Objects detected in the image",
        examples=[["person", "car", "traffic_light", "building"]],
    )
    confidence_score: int = Field(
        ge=0,
        le=100,
        description="Image understanding confidence score",
        examples=[90],
    )
    status: str = Field(
        min_length=1,
        description="Current image understanding status",
        examples=["completed"],
    )
    progress_percentage: int = Field(
        ge=0,
        le=100,
        description="Image understanding progress percentage",
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


class ImageUnderstandingRecordResponse(BaseModel):
    """Image understanding record returned by the API."""

    image_id: str
    image_file: str
    scene_description: str
    detected_objects: list[str]
    confidence_score: int
    status: str
    progress_percentage: int
    created_at: str
    updated_at: str

    @classmethod
    def from_record(
        cls,
        record: ImageUnderstandingRecord,
    ) -> "ImageUnderstandingRecordResponse":
        """Build an API response from a stored image understanding record."""
        return cls(
            image_id=record.image_id,
            image_file=record.image_file,
            scene_description=record.scene_description,
            detected_objects=record.detected_objects,
            confidence_score=record.confidence_score,
            status=record.status,
            progress_percentage=record.progress_percentage,
            created_at=record.created_at,
            updated_at=record.updated_at,
        )


class UserImageUnderstandingAgentResponse(BaseModel):
    """All image understanding records for one user."""

    user_id: str
    image_understanding_records: list[ImageUnderstandingRecordResponse]
