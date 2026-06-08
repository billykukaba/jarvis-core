from fastapi import APIRouter

from app.models.presence import PresenceResponse
from app.services.engine_registry import presence_engine

router = APIRouter(tags=["presence"])


@router.get("/presence/{user_id}", response_model=PresenceResponse)
async def get_presence(user_id: str) -> PresenceResponse:
    record = presence_engine.get_presence_state(user_id)
    return PresenceResponse.from_record(record)


@router.post("/presence/{user_id}/arrive", response_model=PresenceResponse)
async def user_arrived(user_id: str) -> PresenceResponse:
    record = presence_engine.user_arrived(user_id)
    return PresenceResponse.from_record(record)


@router.post("/presence/{user_id}/leave", response_model=PresenceResponse)
async def user_left(user_id: str) -> PresenceResponse:
    record = presence_engine.user_left(user_id)
    return PresenceResponse.from_record(record)
