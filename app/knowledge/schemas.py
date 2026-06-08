from typing import Any

from pydantic import BaseModel, Field

from app.knowledge.knowledge_engine import KnowledgeRecord


class KnowledgeRequest(BaseModel):
    topic: str = Field(min_length=1)
    value: Any


class KnowledgeResponse(BaseModel):
    user_id: str
    topic: str
    value: Any

    @classmethod
    def from_record(cls, record: KnowledgeRecord) -> "KnowledgeResponse":
        return cls(
            user_id=record.user_id,
            topic=record.topic,
            value=record.value,
        )


class UserKnowledgeResponse(BaseModel):
    user_id: str
    knowledge: dict[str, Any]
