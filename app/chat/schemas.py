from datetime import datetime

from pydantic import BaseModel, Field

from app.chat.conversation_history import ConversationMessage


class ChatRequest(BaseModel):
    message: str = Field(min_length=1)


class ChatResponse(BaseModel):
    reply: str


class ConversationMessageResponse(BaseModel):
    role: str
    content: str
    created_at: datetime

    @classmethod
    def from_message(cls, message: ConversationMessage) -> "ConversationMessageResponse":
        return cls(
            role=message.role,
            content=message.content,
            created_at=message.created_at,
        )


class ChatHistoryResponse(BaseModel):
    messages: list[ConversationMessageResponse]
