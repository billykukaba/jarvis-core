from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from threading import Lock
from typing import Any


@dataclass(frozen=True)
class MemoryRecord:
    user_id: str
    key: str
    value: Any


class MemoryEngine:
    def __init__(self, storage_path: Path | None = None) -> None:
        self._storage_path = storage_path or Path("data/memories.json")
        self._lock = Lock()
        self._storage_path.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_storage_file()

    def remember(self, user_id: str, key: str, value: Any) -> MemoryRecord:
        normalized_key = key.strip()

        with self._lock:
            memories = self._read_memories()
            user_memories = memories.setdefault(user_id, {})
            user_memories[normalized_key] = value
            self._write_memories(memories)

        return MemoryRecord(user_id=user_id, key=normalized_key, value=value)

    def recall(self, user_id: str, key: str) -> MemoryRecord | None:
        normalized_key = key.strip()

        with self._lock:
            memories = self._read_memories()
            user_memories = memories.get(user_id, {})

        if normalized_key not in user_memories:
            return None

        return MemoryRecord(
            user_id=user_id,
            key=normalized_key,
            value=user_memories[normalized_key],
        )

    def get_all_memories(self, user_id: str) -> dict[str, Any]:
        with self._lock:
            memories = self._read_memories()
            return dict(memories.get(user_id, {}))

    def _ensure_storage_file(self) -> None:
        if not self._storage_path.exists():
            self._storage_path.write_text("{}", encoding="utf-8")

    def _read_memories(self) -> dict[str, dict[str, Any]]:
        try:
            with self._storage_path.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except json.JSONDecodeError:
            return {}

        if not isinstance(data, dict):
            return {}

        return data

    def _write_memories(self, memories: dict[str, dict[str, Any]]) -> None:
        temporary_path = self._storage_path.with_suffix(".tmp")
        with temporary_path.open("w", encoding="utf-8") as file:
            json.dump(memories, file, indent=2)

        temporary_path.replace(self._storage_path)
