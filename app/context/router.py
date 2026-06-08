from fastapi import APIRouter, HTTPException, status

from app.context.schemas import ContextRequest, ContextResponse
from app.services.engine_registry import context_engine

router = APIRouter(tags=["context"])


@router.post("/context/{user_id}", response_model=ContextResponse)
async def store_context(user_id: str, request: ContextRequest) -> ContextResponse:
    context = context_engine.store_context(user_id, request.to_context())
    return ContextResponse.from_context(user_id, context)


@router.get("/context/{user_id}", response_model=ContextResponse)
async def get_context(user_id: str) -> ContextResponse:
    context = context_engine.get_context(user_id)
    if context is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Context not found",
        )

    return ContextResponse.from_context(user_id, context)


@router.put("/context/{user_id}", response_model=ContextResponse)
async def update_context(user_id: str, request: ContextRequest) -> ContextResponse:
    context = context_engine.update_context(user_id, request.to_context())
    return ContextResponse.from_context(user_id, context)
