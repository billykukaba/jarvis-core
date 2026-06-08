from typing import Any

from pydantic import BaseModel, Field

from app.long_term_memory.long_term_memory_engine import LongTermMemoryRecord


class LongTermMemoryRequest(BaseModel):
    key: str = Field(min_length=1)
    value: Any


class LongTermMemoryUpdateRequest(BaseModel):
    value: Any


class LongTermMemoryResponse(BaseModel):
    user_id: str
    key: str
    value: Any

    @classmethod
    def from_record(
        cls,
        record: LongTermMemoryRecord,
    ) -> "LongTermMemoryResponse":
        return cls(
            user_id=record.user_id,
            key=record.key,
            value=record.value,
        )


class UserLongTermMemoriesResponse(BaseModel):
    user_id: str
    memories: dict[str, Any]


class DeleteLongTermMemoryResponse(BaseModel):
    deleted: bool
    memory: LongTermMemoryResponse
