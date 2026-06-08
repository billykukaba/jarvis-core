from fastapi import APIRouter

from app.models.proactive import ProactiveResponse
from app.services.engine_registry import proactive_engine

router = APIRouter(tags=["proactive"])


@router.get("/proactive/{user_id}", response_model=ProactiveResponse)
async def get_proactive_suggestions(user_id: str) -> ProactiveResponse:
    suggestions = proactive_engine.generate_suggestion(user_id)
    return ProactiveResponse(user_id=user_id, suggestions=suggestions)
