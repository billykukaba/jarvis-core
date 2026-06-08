from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from threading import Lock


class PresenceState(str, Enum):
    ONLINE = "ONLINE"
    AWAY = "AWAY"
    OFFLINE = "OFFLINE"


@dataclass(frozen=True)
class PresenceRecord:
    user_id: str
    state: PresenceState
    last_seen: datetime | None


class PresenceEngine:
    def __init__(self) -> None:
        self._presence: dict[str, PresenceRecord] = {}
        self._lock = Lock()

    def user_arrived(self, user_id: str) -> PresenceRecord:
        record = PresenceRecord(
            user_id=user_id,
            state=PresenceState.ONLINE,
            last_seen=self._now(),
        )
        return self._set_presence(record)

    def user_left(self, user_id: str) -> PresenceRecord:
        record = PresenceRecord(
            user_id=user_id,
            state=PresenceState.OFFLINE,
            last_seen=self._now(),
        )
        return self._set_presence(record)

    def is_user_present(self, user_id: str) -> bool:
        return self.get_presence_state(user_id).state == PresenceState.ONLINE

    def get_presence_state(self, user_id: str) -> PresenceRecord:
        with self._lock:
            return self._presence.get(
                user_id,
                PresenceRecord(
                    user_id=user_id,
                    state=PresenceState.OFFLINE,
                    last_seen=None,
                ),
            )

    def _set_presence(self, record: PresenceRecord) -> PresenceRecord:
        with self._lock:
            self._presence[record.user_id] = record
            return record

    @staticmethod
    def _now() -> datetime:
        return datetime.now(timezone.utc)
