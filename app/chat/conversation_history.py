from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from threading import Lock


@dataclass(frozen=True)
class ConversationMessage:
    role: str
    content: str
    created_at: datetime


class ConversationHistory:
    def __init__(self, limit: int = 50) -> None:
        self._messages: dict[str, list[ConversationMessage]] = {}
        self._limit = limit
        self._lock = Lock()

    def add_message(self, user_id: str, role: str, content: str) -> ConversationMessage:
        message = ConversationMessage(
            role=role,
            content=content,
            created_at=datetime.now(timezone.utc),
        )

        with self._lock:
            messages = self._messages.setdefault(user_id, [])
            messages.append(message)
            self._messages[user_id] = messages[-self._limit :]

        return message

    def get_messages(self, user_id: str) -> list[ConversationMessage]:
        with self._lock:
            return list(self._messages.get(user_id, []))
