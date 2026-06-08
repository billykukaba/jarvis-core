from fastapi import APIRouter

from app.reasoning.schemas import ReasoningRequest, ReasoningResponse
from app.services.engine_registry import reasoning_engine

router = APIRouter(tags=["reasoning"])


@router.post("/reasoning/{user_id}", response_model=ReasoningResponse)
async def reason(user_id: str, request: ReasoningRequest) -> ReasoningResponse:
    answer = reasoning_engine.answer_question(user_id, request.question)
    return ReasoningResponse(answer=answer)
