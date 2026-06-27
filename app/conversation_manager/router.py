"""FastAPI routes for the Conversation Manager (Module 54)."""

from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, status

from app.conversation_manager.conversation_manager_engine import (
    normalize_conversation_id,
)
from app.conversation_manager.schemas import (
    ConversationManagerRecord,
    ConversationManagerRecordResponse,
    UserConversationManagerResponse,
)
from app.services.engine_registry import conversation_manager_engine

# Router exposed to FastAPI as conversation_manager_router in main.py.
conversation_manager_router = APIRouter(tags=["conversation_manager"])


def parse_path_conversation_id(conversation_id: str) -> str:
    """Decode URL path conversation IDs so spaces work in GET, PUT, and DELETE."""
    return unquote(conversation_id.replace("+", " "))


@conversation_manager_router.post(
    "/conversation_manager/{user_id}",
    response_model=ConversationManagerRecordResponse,
    summary="Create conversation record",
    description="Create a new conversation record for the specified user.",
)
async def create_conversation_record(
    user_id: str,
    request: ConversationManagerRecord,
) -> ConversationManagerRecordResponse:
    """Create and return a conversation record."""
    if conversation_manager_engine.conversation_id_exists(
        user_id,
        request.conversation_id,
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Conversation already exists",
        )

    record = conversation_manager_engine.create_record(user_id, request)
    return ConversationManagerRecordResponse.from_record(record)


@conversation_manager_router.get(
    "/conversation_manager/{user_id}",
    response_model=UserConversationManagerResponse,
    summary="Get all conversation records",
    description="Return all conversation records saved by the specified user.",
)
async def get_conversation_records(
    user_id: str,
) -> UserConversationManagerResponse:
    """Return all conversation records for a user."""
    records = conversation_manager_engine.get_records(user_id)
    return UserConversationManagerResponse(
        user_id=user_id,
        conversations=[
            ConversationManagerRecordResponse.from_record(record)
            for record in records
        ],
    )


@conversation_manager_router.get(
    "/conversation_manager/{user_id}/{conversation_id}",
    response_model=ConversationManagerRecordResponse,
    summary="Get one conversation record",
    description="Return one conversation record identified by conversation ID.",
)
async def get_conversation_record(
    user_id: str,
    conversation_id: str,
) -> ConversationManagerRecordResponse:
    """Return a single conversation record by ID."""
    decoded_id = parse_path_conversation_id(conversation_id)
    record = conversation_manager_engine.get_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )

    return ConversationManagerRecordResponse.from_record(record)


@conversation_manager_router.put(
    "/conversation_manager/{user_id}/{conversation_id}",
    response_model=ConversationManagerRecordResponse,
    status_code=status.HTTP_200_OK,
    summary="Update conversation record",
    description="Replace an existing conversation record with updated data.",
)
async def update_conversation_record(
    user_id: str,
    conversation_id: str,
    request: ConversationManagerRecord,
) -> ConversationManagerRecordResponse:
    """Update and return a conversation record."""
    decoded_id = parse_path_conversation_id(conversation_id)

    # Allow keeping the same conversation ID while changing title/status.
    if normalize_conversation_id(request.conversation_id) != normalize_conversation_id(
        decoded_id
    ):
        if conversation_manager_engine.conversation_id_exists(
            user_id,
            request.conversation_id,
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Conversation already exists",
            )

    record = conversation_manager_engine.update_record(
        user_id,
        decoded_id,
        request,
    )
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )

    return ConversationManagerRecordResponse.from_record(record)


@conversation_manager_router.delete(
    "/conversation_manager/{user_id}/{conversation_id}",
    response_model=ConversationManagerRecordResponse,
    summary="Delete conversation record",
    description="Delete a conversation record and return the removed record.",
)
async def delete_conversation_record(
    user_id: str,
    conversation_id: str,
) -> ConversationManagerRecordResponse:
    """Delete a conversation record and return the deleted item."""
    decoded_id = parse_path_conversation_id(conversation_id)
    record = conversation_manager_engine.delete_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )

    return ConversationManagerRecordResponse.from_record(record)
