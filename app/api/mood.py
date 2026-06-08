from fastapi import APIRouter

from app.models.mood import MoodRequest, MoodResponse
from app.services.engine_registry import mood_engine

router = APIRouter(tags=["mood"])


@router.post("/mood/{user_id}", response_model=MoodResponse)
async def update_user_mood(user_id: str, request: MoodRequest) -> MoodResponse:
    record = mood_engine.update_user_mood(user_id, request.text)
    return MoodResponse.from_record(record)


@router.get("/mood/{user_id}", response_model=MoodResponse)
async def get_user_mood(user_id: str) -> MoodResponse:
    record = mood_engine.get_user_mood(user_id)
    return MoodResponse.from_record(record)
