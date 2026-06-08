from fastapi import APIRouter

from app.history.schemas import (
    HistoryEventRequest,
    HistoryEventResponse,
    HistoryResponse,
)
from app.services.engine_registry import history_engine

router = APIRouter(tags=["history"])


@router.post("/history/{user_id}", response_model=HistoryResponse)
async def add_event(user_id: str, request: HistoryEventRequest) -> HistoryResponse:
    history_engine.add_event(user_id, request.event)
    history = history_engine.get_history(user_id)
    return HistoryResponse(
        user_id=user_id,
        history=[HistoryEventResponse.from_event(event) for event in history],
    )


@router.get("/history/{user_id}", response_model=HistoryResponse)
async def get_history(user_id: str) -> HistoryResponse:
    history = history_engine.get_history(user_id)
    return HistoryResponse(
        user_id=user_id,
        history=[HistoryEventResponse.from_event(event) for event in history],
    )
