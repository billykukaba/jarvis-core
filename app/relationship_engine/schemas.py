"""Pydantic schemas for the Relationship Engine."""

from pydantic import BaseModel, ConfigDict, Field


class RelationshipRecord(BaseModel):
    """Relationship record stored for a user."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "relationship_id": "rel_001",
                    "source_entity": "user_billy",
                    "target_entity": "project_jarvis_core",
                    "relationship_type": "owner",
                    "relationship_strength": 95,
                    "relationship_context": "Primary owner and lead developer of the project.",
                    "importance_score": 90,
                    "status": "active",
                    "progress_percentage": 100,
                    "created_at": "2026-06-05T04:00:00",
                    "updated_at": "2026-06-05T04:05:00",
                }
            ]
        }
    )

    relationship_id: str = Field(
        min_length=1,
        description="Unique relationship record identifier",
        examples=["rel_001"],
    )
    source_entity: str = Field(
        min_length=1,
        description="Source entity in the relationship",
        examples=["user_billy"],
    )
    target_entity: str = Field(
        min_length=1,
        description="Target entity in the relationship",
        examples=["project_jarvis_core"],
    )
    relationship_type: str = Field(
        min_length=1,
        description="Type of relationship between entities",
        examples=["owner"],
    )
    relationship_strength: int = Field(
        ge=0,
        le=100,
        description="Strength score of the relationship",
        examples=[95],
    )
    relationship_context: str = Field(
        min_length=1,
        description="Contextual description of the relationship",
        examples=["Primary owner and lead developer of the project."],
    )
    importance_score: int = Field(
        ge=0,
        le=100,
        description="Importance score of the relationship",
        examples=[90],
    )
    status: str = Field(
        min_length=1,
        description="Current relationship record status",
        examples=["active"],
    )
    progress_percentage: int = Field(
        ge=0,
        le=100,
        description="Relationship record progress percentage",
        examples=[100],
    )
    created_at: str = Field(
        min_length=1,
        description="Record creation timestamp",
        examples=["2026-06-05T04:00:00"],
    )
    updated_at: str = Field(
        min_length=1,
        description="Record last update timestamp",
        examples=["2026-06-05T04:05:00"],
    )


class RelationshipRecordResponse(BaseModel):
    """Relationship record returned by the API."""

    relationship_id: str
    source_entity: str
    target_entity: str
    relationship_type: str
    relationship_strength: int
    relationship_context: str
    importance_score: int
    status: str
    progress_percentage: int
    created_at: str
    updated_at: str

    @classmethod
    def from_record(
        cls,
        record: RelationshipRecord,
    ) -> "RelationshipRecordResponse":
        """Build an API response from a stored relationship record."""
        return cls(
            relationship_id=record.relationship_id,
            source_entity=record.source_entity,
            target_entity=record.target_entity,
            relationship_type=record.relationship_type,
            relationship_strength=record.relationship_strength,
            relationship_context=record.relationship_context,
            importance_score=record.importance_score,
            status=record.status,
            progress_percentage=record.progress_percentage,
            created_at=record.created_at,
            updated_at=record.updated_at,
        )


class UserRelationshipEngineResponse(BaseModel):
    """All relationship records for one user."""

    user_id: str
    relationship_records: list[RelationshipRecordResponse]
