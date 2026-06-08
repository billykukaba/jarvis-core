from fastapi import APIRouter, HTTPException, status

from app.knowledge.schemas import (
    KnowledgeRequest,
    KnowledgeResponse,
    UserKnowledgeResponse,
)
from app.services.engine_registry import knowledge_engine

router = APIRouter(tags=["knowledge"])


@router.post("/knowledge/{user_id}", response_model=KnowledgeResponse)
async def store_knowledge(
    user_id: str,
    request: KnowledgeRequest,
) -> KnowledgeResponse:
    record = knowledge_engine.store_knowledge(
        user_id=user_id,
        topic=request.topic,
        value=request.value,
    )
    return KnowledgeResponse.from_record(record)


@router.get("/knowledge/{user_id}", response_model=UserKnowledgeResponse)
async def get_all_knowledge(user_id: str) -> UserKnowledgeResponse:
    knowledge = knowledge_engine.get_all_knowledge(user_id)
    return UserKnowledgeResponse(user_id=user_id, knowledge=knowledge)


@router.get("/knowledge/{user_id}/{topic}", response_model=KnowledgeResponse)
async def get_knowledge(user_id: str, topic: str) -> KnowledgeResponse:
    record = knowledge_engine.get_knowledge(user_id, topic)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Knowledge not found",
        )

    return KnowledgeResponse.from_record(record)
