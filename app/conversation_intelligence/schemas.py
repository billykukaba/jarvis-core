"""Pydantic schemas for the Conversation Intelligence module (Module 55)."""

from pydantic import BaseModel, ConfigDict, Field


class ConversationIntelligenceRecord(BaseModel):
    """Conversation intelligence record stored for a user."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "intelligence_id": "intel_001",
                    "sentiment": "Positive",
                    "summary": "User discussed AI project planning",
                }
            ]
        }
    )

    intelligence_id: str = Field(
        min_length=1,
        description="Unique intelligence record identifier",
        examples=["intel_001"],
    )
    sentiment: str = Field(
        min_length=1,
        description="Detected conversation sentiment",
        examples=["Positive"],
    )
    summary: str = Field(
        min_length=1,
        description="Conversation intelligence summary",
        examples=["User discussed AI project planning"],
    )


class ConversationIntelligenceRecordResponse(BaseModel):
    """Conversation intelligence record returned by the API."""

    intelligence_id: str
    sentiment: str
    summary: str

    @classmethod
    def from_record(
        cls,
        record: ConversationIntelligenceRecord,
    ) -> "ConversationIntelligenceRecordResponse":
        """Build an API response from a stored intelligence record."""
        return cls(
            intelligence_id=record.intelligence_id,
            sentiment=record.sentiment,
            summary=record.summary,
        )


class UserConversationIntelligenceResponse(BaseModel):
    """All conversation intelligence records for one user."""

    user_id: str
    conversation_intelligence: list[ConversationIntelligenceRecordResponse]
