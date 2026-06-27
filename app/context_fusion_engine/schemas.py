"""Pydantic schemas for the Context Fusion Engine."""

from pydantic import BaseModel, ConfigDict, Field


class ContextFusionRecord(BaseModel):
    """Context fusion record stored for a user."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "fusion_id": "fusion_001",
                    "context_sources": [
                        "conversation_history",
                        "long_term_memory",
                        "user_goals",
                        "emotional_state",
                    ],
                    "current_context": "User is planning a product launch meeting.",
                    "long_term_memory_context": "User prefers concise technical summaries.",
                    "user_goal_context": "Prepare launch timeline and stakeholder updates.",
                    "emotional_context": "Focused and motivated.",
                    "fusion_summary": "User needs a structured launch plan with technical clarity.",
                    "confidence_score": 91,
                    "status": "completed",
                    "progress_percentage": 100,
                    "created_at": "2026-06-05T03:00:00",
                    "updated_at": "2026-06-05T03:08:00",
                }
            ]
        }
    )

    fusion_id: str = Field(
        min_length=1,
        description="Unique context fusion record identifier",
        examples=["fusion_001"],
    )
    context_sources: list[str] = Field(
        min_length=1,
        description="Sources combined into the fused context",
        examples=[
            [
                "conversation_history",
                "long_term_memory",
                "user_goals",
                "emotional_state",
            ]
        ],
    )
    current_context: str = Field(
        min_length=1,
        description="Current conversational or situational context",
        examples=["User is planning a product launch meeting."],
    )
    long_term_memory_context: str = Field(
        min_length=1,
        description="Relevant long-term memory context",
        examples=["User prefers concise technical summaries."],
    )
    user_goal_context: str = Field(
        min_length=1,
        description="User goal context applied to the fusion",
        examples=["Prepare launch timeline and stakeholder updates."],
    )
    emotional_context: str = Field(
        min_length=1,
        description="Emotional context applied to the fusion",
        examples=["Focused and motivated."],
    )
    fusion_summary: str = Field(
        min_length=1,
        description="Unified summary of the fused context layers",
        examples=["User needs a structured launch plan with technical clarity."],
    )
    confidence_score: int = Field(
        ge=0,
        le=100,
        description="Context fusion confidence score",
        examples=[91],
    )
    status: str = Field(
        min_length=1,
        description="Current context fusion status",
        examples=["completed"],
    )
    progress_percentage: int = Field(
        ge=0,
        le=100,
        description="Context fusion progress percentage",
        examples=[100],
    )
    created_at: str = Field(
        min_length=1,
        description="Record creation timestamp",
        examples=["2026-06-05T03:00:00"],
    )
    updated_at: str = Field(
        min_length=1,
        description="Record last update timestamp",
        examples=["2026-06-05T03:08:00"],
    )


class ContextFusionRecordResponse(BaseModel):
    """Context fusion record returned by the API."""

    fusion_id: str
    context_sources: list[str]
    current_context: str
    long_term_memory_context: str
    user_goal_context: str
    emotional_context: str
    fusion_summary: str
    confidence_score: int
    status: str
    progress_percentage: int
    created_at: str
    updated_at: str

    @classmethod
    def from_record(
        cls,
        record: ContextFusionRecord,
    ) -> "ContextFusionRecordResponse":
        """Build an API response from a stored context fusion record."""
        return cls(
            fusion_id=record.fusion_id,
            context_sources=record.context_sources,
            current_context=record.current_context,
            long_term_memory_context=record.long_term_memory_context,
            user_goal_context=record.user_goal_context,
            emotional_context=record.emotional_context,
            fusion_summary=record.fusion_summary,
            confidence_score=record.confidence_score,
            status=record.status,
            progress_percentage=record.progress_percentage,
            created_at=record.created_at,
            updated_at=record.updated_at,
        )


class UserContextFusionEngineResponse(BaseModel):
    """All context fusion records for one user."""

    user_id: str
    context_fusion_records: list[ContextFusionRecordResponse]
