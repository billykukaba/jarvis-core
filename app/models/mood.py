from pydantic import BaseModel, Field

from app.consciousness.mood_engine import MoodRecord


class MoodRequest(BaseModel):
    text: str = Field(min_length=1)


class MoodResponse(BaseModel):
    user_id: str
    mood: str

    @classmethod
    def from_record(cls, record: MoodRecord) -> "MoodResponse":
        return cls(
            user_id=record.user_id,
            mood=record.mood.value,
        )
