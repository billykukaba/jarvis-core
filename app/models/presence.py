from datetime import datetime

from pydantic import BaseModel

from app.consciousness.presence_engine import PresenceRecord


class PresenceResponse(BaseModel):
    user_id: str
    state: str
    last_seen: datetime | None

    @classmethod
    def from_record(cls, record: PresenceRecord) -> "PresenceResponse":
        return cls(
            user_id=record.user_id,
            state=record.state.value,
            last_seen=record.last_seen,
        )
