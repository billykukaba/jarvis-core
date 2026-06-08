from fastapi import APIRouter

from app.brain.schemas import BrainRequest, BrainResponse
from app.services.engine_registry import brain_engine

router = APIRouter(tags=["brain"])


@router.post("/brain/{user_id}", response_model=BrainResponse)
async def process_message(user_id: str, request: BrainRequest) -> BrainResponse:
    result = brain_engine.process_message(user_id, request.message)
    return BrainResponse.from_result(result)
