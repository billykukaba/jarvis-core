from pydantic import BaseModel, Field

from app.consciousness.habit_engine import HabitPrediction, HabitRecord


class HabitRecordRequest(BaseModel):
    activity: str = Field(min_length=1)


class HabitResponse(BaseModel):
    user_id: str
    activity: str
    hour: int
    frequency_count: int

    @classmethod
    def from_record(cls, record: HabitRecord) -> "HabitResponse":
        return cls(
            user_id=record.user_id,
            activity=record.activity,
            hour=record.hour,
            frequency_count=record.frequency_count,
        )


class HabitPredictionResponse(BaseModel):
    predicted_activity: str | None
    confidence: float

    @classmethod
    def from_prediction(cls, prediction: HabitPrediction) -> "HabitPredictionResponse":
        return cls(
            predicted_activity=prediction.predicted_activity,
            confidence=round(prediction.confidence, 2),
        )
