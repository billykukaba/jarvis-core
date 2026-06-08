from fastapi import APIRouter

from app.decision.schemas import DecisionRequest, DecisionResponse
from app.services.engine_registry import decision_engine

router = APIRouter(tags=["decision"])


@router.post("/decision/{user_id}", response_model=DecisionResponse)
async def make_decision(user_id: str, request: DecisionRequest) -> DecisionResponse:
    result = decision_engine.make_decision(user_id, request.question)
    return DecisionResponse.from_result(result)
