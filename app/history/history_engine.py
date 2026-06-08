from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from threading import Lock


@dataclass(frozen=True)
class HistoryEvent:
    event: str
    timestamp: datetime


class HistoryEngine:
    def __init__(self) -> None:
        self._history: dict[str, list[HistoryEvent]] = {}
        self._lock = Lock()

    def add_event(self, user_id: str, event: str) -> HistoryEvent:
        history_event = HistoryEvent(
            event=event.strip(),
            timestamp=datetime.now(timezone.utc),
        )

        with self._lock:
            self._history.setdefault(user_id, []).append(history_event)

        return history_event

    def get_history(self, user_id: str) -> list[HistoryEvent]:
        with self._lock:
            return list(self._history.get(user_id, []))
