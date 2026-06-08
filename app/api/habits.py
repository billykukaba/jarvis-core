from fastapi import APIRouter

from app.models.habit import (
    HabitPredictionResponse,
    HabitRecordRequest,
    HabitResponse,
)
from app.services.engine_registry import habit_engine

router = APIRouter(tags=["habits"])


@router.post("/habits/{user_id}/record", response_model=HabitResponse)
async def record_activity(user_id: str, request: HabitRecordRequest) -> HabitResponse:
    record = habit_engine.record_activity(user_id, request.activity)
    return HabitResponse.from_record(record)


@router.get("/habits/{user_id}", response_model=list[HabitResponse])
async def get_habits(user_id: str) -> list[HabitResponse]:
    records = habit_engine.get_habits(user_id)
    return [HabitResponse.from_record(record) for record in records]


@router.get("/habits/{user_id}/predict", response_model=HabitPredictionResponse)
async def predict_next_activity(user_id: str) -> HabitPredictionResponse:
    prediction = habit_engine.predict_next_activity(user_id)
    return HabitPredictionResponse.from_prediction(prediction)
