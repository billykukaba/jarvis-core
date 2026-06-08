from __future__ import annotations

from dataclasses import dataclass
from threading import Lock
from typing import Any


@dataclass(frozen=True)
class LongTermMemoryRecord:
    user_id: str
    key: str
    value: Any


class LongTermMemoryEngine:
    def __init__(self) -> None:
        self._memories: dict[str, dict[str, Any]] = {}
        self._lock = Lock()

    def store_memory(self, user_id: str, key: str, value: Any) -> LongTermMemoryRecord:
        normalized_key = key.strip()

        with self._lock:
            user_memories = self._memories.setdefault(user_id, {})
            user_memories[normalized_key] = value

        return LongTermMemoryRecord(
            user_id=user_id,
            key=normalized_key,
            value=value,
        )

    def retrieve_memory(self, user_id: str, key: str) -> LongTermMemoryRecord | None:
        normalized_key = key.strip()

        with self._lock:
            user_memories = self._memories.get(user_id, {})
            if normalized_key not in user_memories:
                return None

            value = user_memories[normalized_key]

        return LongTermMemoryRecord(
            user_id=user_id,
            key=normalized_key,
            value=value,
        )

    def get_all_memories(self, user_id: str) -> dict[str, Any]:
        with self._lock:
            return dict(self._memories.get(user_id, {}))

    def update_memory(
        self,
        user_id: str,
        key: str,
        value: Any,
    ) -> LongTermMemoryRecord | None:
        normalized_key = key.strip()

        with self._lock:
            user_memories = self._memories.get(user_id)
            if user_memories is None or normalized_key not in user_memories:
                return None

            user_memories[normalized_key] = value

        return LongTermMemoryRecord(
            user_id=user_id,
            key=normalized_key,
            value=value,
        )

    def delete_memory(self, user_id: str, key: str) -> LongTermMemoryRecord | None:
        normalized_key = key.strip()

        with self._lock:
            user_memories = self._memories.get(user_id)
            if user_memories is None or normalized_key not in user_memories:
                return None

            value = user_memories.pop(normalized_key)

        return LongTermMemoryRecord(
            user_id=user_id,
            key=normalized_key,
            value=value,
        )
