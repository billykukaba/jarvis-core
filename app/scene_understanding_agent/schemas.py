"""Pydantic schemas for the Scene Understanding Agent."""

from pydantic import BaseModel, ConfigDict, Field


class SceneUnderstandingRecord(BaseModel):
    """Scene understanding record stored for a user."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "scene_id": "scene_001",
                    "image_file": "office_workspace.jpg",
                    "scene_type": "indoor_office",
                    "scene_description": "Modern office with desk, monitor, and natural lighting.",
                    "detected_entities": ["desk", "monitor", "chair", "window", "plant"],
                    "environment_type": "workplace",
                    "confidence_score": 91,
                    "scene_status": "completed",
                    "progress_percentage": 100,
                    "created_at": "2026-06-04T12:00:00",
                    "updated_at": "2026-06-04T12:05:00",
                }
            ]
        }
    )

    scene_id: str = Field(
        min_length=1,
        description="Unique scene understanding record identifier",
        examples=["scene_001"],
    )
    image_file: str = Field(
        min_length=1,
        description="Source image file name or path",
        examples=["office_workspace.jpg"],
    )
    scene_type: str = Field(
        min_length=1,
        description="Classified scene type",
        examples=["indoor_office"],
    )
    scene_description: str = Field(
        min_length=1,
        description="Natural language description of the scene",
        examples=["Modern office with desk, monitor, and natural lighting."],
    )
    detected_entities: list[str] = Field(
        min_length=1,
        description="Entities detected within the scene",
        examples=[["desk", "monitor", "chair", "window", "plant"]],
    )
    environment_type: str = Field(
        min_length=1,
        description="Environment classification for the scene",
        examples=["workplace"],
    )
    confidence_score: int = Field(
        ge=0,
        le=100,
        description="Scene understanding confidence score",
        examples=[91],
    )
    scene_status: str = Field(
        min_length=1,
        description="Current scene understanding status",
        examples=["completed"],
    )
    progress_percentage: int = Field(
        ge=0,
        le=100,
        description="Scene understanding progress percentage",
        examples=[100],
    )
    created_at: str = Field(
        min_length=1,
        description="Record creation timestamp",
        examples=["2026-06-04T12:00:00"],
    )
    updated_at: str = Field(
        min_length=1,
        description="Record last update timestamp",
        examples=["2026-06-04T12:05:00"],
    )


class SceneUnderstandingRecordResponse(BaseModel):
    """Scene understanding record returned by the API."""

    scene_id: str
    image_file: str
    scene_type: str
    scene_description: str
    detected_entities: list[str]
    environment_type: str
    confidence_score: int
    scene_status: str
    progress_percentage: int
    created_at: str
    updated_at: str

    @classmethod
    def from_record(
        cls,
        record: SceneUnderstandingRecord,
    ) -> "SceneUnderstandingRecordResponse":
        """Build an API response from a stored scene understanding record."""
        return cls(
            scene_id=record.scene_id,
            image_file=record.image_file,
            scene_type=record.scene_type,
            scene_description=record.scene_description,
            detected_entities=record.detected_entities,
            environment_type=record.environment_type,
            confidence_score=record.confidence_score,
            scene_status=record.scene_status,
            progress_percentage=record.progress_percentage,
            created_at=record.created_at,
            updated_at=record.updated_at,
        )


class UserSceneUnderstandingAgentResponse(BaseModel):
    """All scene understanding records for one user."""

    user_id: str
    scene_understanding_records: list[SceneUnderstandingRecordResponse]
