"""Pydantic schemas for the Object Detection Agent."""

from pydantic import BaseModel, ConfigDict, Field


class ObjectDetectionRecord(BaseModel):
    """Object detection record stored for a user."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "object_id": "object_001",
                    "image_file": "street_scene.jpg",
                    "detected_object": "car",
                    "object_category": "vehicle",
                    "confidence_score": 94,
                    "bounding_box": "120,80,340,260",
                    "object_status": "detected",
                    "progress_percentage": 100,
                    "created_at": "2026-06-04T11:00:00",
                    "updated_at": "2026-06-04T11:02:00",
                }
            ]
        }
    )

    object_id: str = Field(
        min_length=1,
        description="Unique object detection record identifier",
        examples=["object_001"],
    )
    image_file: str = Field(
        min_length=1,
        description="Source image file name or path",
        examples=["street_scene.jpg"],
    )
    detected_object: str = Field(
        min_length=1,
        description="Name of the detected object",
        examples=["car"],
    )
    object_category: str = Field(
        min_length=1,
        description="Category classification of the detected object",
        examples=["vehicle"],
    )
    confidence_score: int = Field(
        ge=0,
        le=100,
        description="Object detection confidence score",
        examples=[94],
    )
    bounding_box: str = Field(
        min_length=1,
        description="Bounding box coordinates for the detected object",
        examples=["120,80,340,260"],
    )
    object_status: str = Field(
        min_length=1,
        description="Current object detection status",
        examples=["detected"],
    )
    progress_percentage: int = Field(
        ge=0,
        le=100,
        description="Object detection progress percentage",
        examples=[100],
    )
    created_at: str = Field(
        min_length=1,
        description="Record creation timestamp",
        examples=["2026-06-04T11:00:00"],
    )
    updated_at: str = Field(
        min_length=1,
        description="Record last update timestamp",
        examples=["2026-06-04T11:02:00"],
    )


class ObjectDetectionRecordResponse(BaseModel):
    """Object detection record returned by the API."""

    object_id: str
    image_file: str
    detected_object: str
    object_category: str
    confidence_score: int
    bounding_box: str
    object_status: str
    progress_percentage: int
    created_at: str
    updated_at: str

    @classmethod
    def from_record(
        cls,
        record: ObjectDetectionRecord,
    ) -> "ObjectDetectionRecordResponse":
        """Build an API response from a stored object detection record."""
        return cls(
            object_id=record.object_id,
            image_file=record.image_file,
            detected_object=record.detected_object,
            object_category=record.object_category,
            confidence_score=record.confidence_score,
            bounding_box=record.bounding_box,
            object_status=record.object_status,
            progress_percentage=record.progress_percentage,
            created_at=record.created_at,
            updated_at=record.updated_at,
        )


class UserObjectDetectionAgentResponse(BaseModel):
    """All object detection records for one user."""

    user_id: str
    object_detection_records: list[ObjectDetectionRecordResponse]
