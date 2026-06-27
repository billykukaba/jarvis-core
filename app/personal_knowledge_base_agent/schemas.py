"""Pydantic schemas for the Personal Knowledge Base Agent."""

from pydantic import BaseModel, ConfigDict, Field


class PersonalKnowledgeRecord(BaseModel):
    """Personal knowledge record stored for a user."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "knowledge_base_id": "kb_001",
                    "knowledge_title": "FastAPI Best Practices",
                    "knowledge_category": "programming",
                    "knowledge_content": "Use dependency injection and Pydantic models for validation.",
                    "knowledge_source": "internal_notes.md",
                    "related_tags": ["fastapi", "python", "api-design"],
                    "importance_score": 85,
                    "status": "active",
                    "progress_percentage": 100,
                    "created_at": "2026-06-04T17:00:00",
                    "updated_at": "2026-06-04T17:05:00",
                }
            ]
        }
    )

    knowledge_base_id: str = Field(
        min_length=1,
        description="Unique personal knowledge record identifier",
        examples=["kb_001"],
    )
    knowledge_title: str = Field(
        min_length=1,
        description="Title of the knowledge entry",
        examples=["FastAPI Best Practices"],
    )
    knowledge_category: str = Field(
        min_length=1,
        description="Category classification of the knowledge entry",
        examples=["programming"],
    )
    knowledge_content: str = Field(
        min_length=1,
        description="Main content of the knowledge entry",
        examples=["Use dependency injection and Pydantic models for validation."],
    )
    knowledge_source: str = Field(
        min_length=1,
        description="Source of the knowledge entry",
        examples=["internal_notes.md"],
    )
    related_tags: list[str] = Field(
        min_length=1,
        description="Tags related to the knowledge entry",
        examples=[["fastapi", "python", "api-design"]],
    )
    importance_score: int = Field(
        ge=0,
        le=100,
        description="Importance score of the knowledge entry",
        examples=[85],
    )
    status: str = Field(
        min_length=1,
        description="Current knowledge entry status",
        examples=["active"],
    )
    progress_percentage: int = Field(
        ge=0,
        le=100,
        description="Knowledge entry progress percentage",
        examples=[100],
    )
    created_at: str = Field(
        min_length=1,
        description="Record creation timestamp",
        examples=["2026-06-04T17:00:00"],
    )
    updated_at: str = Field(
        min_length=1,
        description="Record last update timestamp",
        examples=["2026-06-04T17:05:00"],
    )


class PersonalKnowledgeRecordResponse(BaseModel):
    """Personal knowledge record returned by the API."""

    knowledge_base_id: str
    knowledge_title: str
    knowledge_category: str
    knowledge_content: str
    knowledge_source: str
    related_tags: list[str]
    importance_score: int
    status: str
    progress_percentage: int
    created_at: str
    updated_at: str

    @classmethod
    def from_record(
        cls,
        record: PersonalKnowledgeRecord,
    ) -> "PersonalKnowledgeRecordResponse":
        """Build an API response from a stored personal knowledge record."""
        return cls(
            knowledge_base_id=record.knowledge_base_id,
            knowledge_title=record.knowledge_title,
            knowledge_category=record.knowledge_category,
            knowledge_content=record.knowledge_content,
            knowledge_source=record.knowledge_source,
            related_tags=record.related_tags,
            importance_score=record.importance_score,
            status=record.status,
            progress_percentage=record.progress_percentage,
            created_at=record.created_at,
            updated_at=record.updated_at,
        )


class UserPersonalKnowledgeBaseAgentResponse(BaseModel):
    """All personal knowledge records for one user."""

    user_id: str
    knowledge_base_records: list[PersonalKnowledgeRecordResponse]
