"""Pydantic schemas for the Conversation Manager (Module 54)."""

from pydantic import BaseModel, ConfigDict, Field


class ConversationManagerRecord(BaseModel):
    """Conversation record stored for a user."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "conversation_id": "conv-001",
                    "title": "MIT Planning",
                    "status": "active",
                }
            ]
        }
    )

    conversation_id: str = Field(
        min_length=1,
        description="Unique conversation identifier",
        examples=["conv-001"],
    )
    title: str = Field(
        min_length=1,
        description="Conversation title",
        examples=["MIT Planning"],
    )
    status: str = Field(
        min_length=1,
        description="Conversation status",
        examples=["active"],
    )


class ConversationManagerRecordResponse(BaseModel):
    """Conversation record returned by the API."""

    conversation_id: str
    title: str
    status: str

    @classmethod
    def from_record(
        cls,
        record: ConversationManagerRecord,
    ) -> "ConversationManagerRecordResponse":
        """Build an API response from a stored conversation record."""
        return cls(
            conversation_id=record.conversation_id,
            title=record.title,
            status=record.status,
        )


class UserConversationManagerResponse(BaseModel):
    """All conversation records for one user."""

    user_id: str
    conversations: list[ConversationManagerRecordResponse]
