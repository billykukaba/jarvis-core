from datetime import datetime

from pydantic import BaseModel, Field

from app.history.history_engine import HistoryEvent


class HistoryEventRequest(BaseModel):
    event: str = Field(min_length=1)


class HistoryEventResponse(BaseModel):
    event: str
    timestamp: datetime

    @classmethod
    def from_event(cls, event: HistoryEvent) -> "HistoryEventResponse":
        return cls(
            event=event.event,
            timestamp=event.timestamp,
        )


class HistoryResponse(BaseModel):
    user_id: str
    history: list[HistoryEventResponse]
