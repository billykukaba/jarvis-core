from typing import Any

from pydantic import BaseModel, Field

from app.memory.memory_engine import MemoryRecord


class MemoryRequest(BaseModel):
    key: str = Field(min_length=1)
    value: Any


class MemoryResponse(BaseModel):
    user_id: str
    key: str
    value: Any

    @classmethod
    def from_record(cls, record: MemoryRecord) -> "MemoryResponse":
        return cls(
            user_id=record.user_id,
            key=record.key,
            value=record.value,
        )


class UserMemoriesResponse(BaseModel):
    user_id: str
    memories: dict[str, Any]
