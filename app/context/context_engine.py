from __future__ import annotations

from dataclasses import dataclass
from threading import Lock


@dataclass(frozen=True)
class UserContext:
    current_topic: str
    current_task: str
    current_project: str
    notes: str


class ContextEngine:
    def __init__(self) -> None:
        self._contexts: dict[str, UserContext] = {}
        self._lock = Lock()

    def store_context(self, user_id: str, context: UserContext) -> UserContext:
        with self._lock:
            self._contexts[user_id] = context

        return context

    def get_context(self, user_id: str) -> UserContext | None:
        with self._lock:
            return self._contexts.get(user_id)

    def update_context(self, user_id: str, context: UserContext) -> UserContext:
        return self.store_context(user_id, context)
