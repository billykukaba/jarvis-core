from __future__ import annotations

from dataclasses import dataclass
from threading import Lock


@dataclass(frozen=True)
class UserState:
    level: str
    target: str
    current_focus: str
    current_project: str
    status: str


class UserStateEngine:
    def __init__(self) -> None:
        self._states: dict[str, UserState] = {}
        self._lock = Lock()

    def set_state(self, user_id: str, state: UserState) -> UserState:
        with self._lock:
            self._states[user_id] = state

        return state

    def get_state(self, user_id: str) -> UserState | None:
        with self._lock:
            return self._states.get(user_id)

    def update_state(self, user_id: str, state: UserState) -> UserState:
        return self.set_state(user_id, state)
