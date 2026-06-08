from fastapi import APIRouter

from app.chat.schemas import (
    ChatHistoryResponse,
    ChatRequest,
    ChatResponse,
    ConversationMessageResponse,
)
from app.services.engine_registry import chat_engine

router = APIRouter(tags=["chat"])


@router.post("/chat/{user_id}", response_model=ChatResponse)
async def chat(user_id: str, request: ChatRequest) -> ChatResponse:
    reply = chat_engine.generate_reply(user_id, request.message)
    return ChatResponse(reply=reply)


@router.get("/chat/{user_id}/history", response_model=ChatHistoryResponse)
async def get_chat_history(user_id: str) -> ChatHistoryResponse:
    messages = chat_engine.get_history(user_id)
    return ChatHistoryResponse(
        messages=[
            ConversationMessageResponse.from_message(message)
            for message in messages
        ]
    )
