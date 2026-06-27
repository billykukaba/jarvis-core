"""Pydantic schemas for the Face Recognition Agent."""

from pydantic import BaseModel, ConfigDict, Field


class FaceRecognition(BaseModel):
    """Face recognition record stored for a user."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "face_id": "face_001",
                    "image_file": "portrait.jpg",
                    "person_name": "Alice Johnson",
                    "confidence_score": 94,
                    "status": "recognized",
                    "progress_percentage": 100,
                    "created_at": "2026-06-04T09:00:00",
                    "updated_at": "2026-06-04T09:01:00",
                }
            ]
        }
    )

    face_id: str = Field(
        min_length=1,
        description="Unique face record identifier",
        examples=["face_001"],
    )
    image_file: str = Field(
        min_length=1,
        description="Image file name or path",
        examples=["portrait.jpg"],
    )
    person_name: str = Field(
        min_length=1,
        description="Identified person name",
        examples=["Alice Johnson"],
    )
    confidence_score: int = Field(
        ge=0,
        le=100,
        description="Face recognition confidence score",
        examples=[94],
    )
    status: str = Field(
        min_length=1,
        description="Current face recognition status",
        examples=["recognized"],
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


class FaceRecognitionResponse(BaseModel):
    """Face recognition record returned by the API."""

    face_id: str
    image_file: str
    person_name: str
    confidence_score: int
    status: str
    progress_percentage: int
    created_at: str
    updated_at: str

    @classmethod
    def from_face(cls, face: FaceRecognition) -> "FaceRecognitionResponse":
        """Build an API response from a stored face recognition record."""
        return cls(
            face_id=face.face_id,
            image_file=face.image_file,
            person_name=face.person_name,
            confidence_score=face.confidence_score,
            status=face.status,
            progress_percentage=face.progress_percentage,
            created_at=face.created_at,
            updated_at=face.updated_at,
        )


class UserFaceRecognitionAgentResponse(BaseModel):
    """All face recognition records for one user."""

    user_id: str
    face_records: list[FaceRecognitionResponse]
