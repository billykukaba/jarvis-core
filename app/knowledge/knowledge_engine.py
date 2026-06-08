from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from threading import Lock
from typing import Any


@dataclass(frozen=True)
class KnowledgeRecord:
    user_id: str
    topic: str
    value: Any


class KnowledgeEngine:
    def __init__(self, storage_path: Path | None = None) -> None:
        self._storage_path = storage_path or Path("data/knowledge.json")
        self._lock = Lock()
        self._storage_path.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_storage_file()

    def store_knowledge(self, user_id: str, topic: str, value: Any) -> KnowledgeRecord:
        normalized_topic = topic.strip()

        with self._lock:
            knowledge = self._read_knowledge()
            user_knowledge = knowledge.setdefault(user_id, {})
            user_knowledge[normalized_topic] = value
            self._write_knowledge(knowledge)

        return KnowledgeRecord(
            user_id=user_id,
            topic=normalized_topic,
            value=value,
        )

    def get_knowledge(self, user_id: str, topic: str) -> KnowledgeRecord | None:
        normalized_topic = topic.strip()

        with self._lock:
            knowledge = self._read_knowledge()
            user_knowledge = knowledge.get(user_id, {})

        if normalized_topic not in user_knowledge:
            return None

        return KnowledgeRecord(
            user_id=user_id,
            topic=normalized_topic,
            value=user_knowledge[normalized_topic],
        )

    def get_all_knowledge(self, user_id: str) -> dict[str, Any]:
        with self._lock:
            knowledge = self._read_knowledge()
            return dict(knowledge.get(user_id, {}))

    def _ensure_storage_file(self) -> None:
        if not self._storage_path.exists():
            self._storage_path.write_text("{}", encoding="utf-8")

    def _read_knowledge(self) -> dict[str, dict[str, Any]]:
        try:
            with self._storage_path.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except json.JSONDecodeError:
            return {}

        if not isinstance(data, dict):
            return {}

        return data

    def _write_knowledge(self, knowledge: dict[str, dict[str, Any]]) -> None:
        temporary_path = self._storage_path.with_suffix(".tmp")
        with temporary_path.open("w", encoding="utf-8") as file:
            json.dump(knowledge, file, indent=2)

        temporary_path.replace(self._storage_path)
