"""FastAPI routes for the Conversation Intelligence module (Module 55)."""

from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, status

from app.conversation_intelligence.conversation_intelligence_engine import (
    normalize_intelligence_id,
)
from app.conversation_intelligence.schemas import (
    ConversationIntelligenceRecord,
    ConversationIntelligenceRecordResponse,
    UserConversationIntelligenceResponse,
)
from app.services.engine_registry import conversation_intelligence_engine

# Router exposed to FastAPI as conversation_intelligence_router in main.py.
conversation_intelligence_router = APIRouter(tags=["conversation_intelligence"])


def parse_path_intelligence_id(intelligence_id: str) -> str:
    """Decode URL path intelligence IDs so spaces work in GET, PUT, and DELETE."""
    return unquote(intelligence_id.replace("+", " "))


@conversation_intelligence_router.post(
    "/conversation_intelligence/{user_id}",
    response_model=ConversationIntelligenceRecordResponse,
    summary="Create conversation intelligence record",
    description="Create a new conversation intelligence record for the specified user.",
)
async def create_conversation_intelligence_record(
    user_id: str,
    request: ConversationIntelligenceRecord,
) -> ConversationIntelligenceRecordResponse:
    """Create and return a conversation intelligence record."""
    if conversation_intelligence_engine.intelligence_id_exists(
        user_id,
        request.intelligence_id,
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Intelligence already exists",
        )

    record = conversation_intelligence_engine.create_record(user_id, request)
    return ConversationIntelligenceRecordResponse.from_record(record)


@conversation_intelligence_router.get(
    "/conversation_intelligence/{user_id}",
    response_model=UserConversationIntelligenceResponse,
    summary="Get all conversation intelligence records",
    description="Return all conversation intelligence records saved by the specified user.",
)
async def get_conversation_intelligence_records(
    user_id: str,
) -> UserConversationIntelligenceResponse:
    """Return all conversation intelligence records for a user."""
    records = conversation_intelligence_engine.get_records(user_id)
    return UserConversationIntelligenceResponse(
        user_id=user_id,
        conversation_intelligence=[
            ConversationIntelligenceRecordResponse.from_record(record)
            for record in records
        ],
    )


@conversation_intelligence_router.get(
    "/conversation_intelligence/{user_id}/{intelligence_id}",
    response_model=ConversationIntelligenceRecordResponse,
    summary="Get one conversation intelligence record",
    description="Return one conversation intelligence record identified by intelligence ID.",
)
async def get_conversation_intelligence_record(
    user_id: str,
    intelligence_id: str,
) -> ConversationIntelligenceRecordResponse:
    """Return a single conversation intelligence record by ID."""
    decoded_id = parse_path_intelligence_id(intelligence_id)
    record = conversation_intelligence_engine.get_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Intelligence not found",
        )

    return ConversationIntelligenceRecordResponse.from_record(record)


@conversation_intelligence_router.put(
    "/conversation_intelligence/{user_id}/{intelligence_id}",
    response_model=ConversationIntelligenceRecordResponse,
    status_code=status.HTTP_200_OK,
    summary="Update conversation intelligence record",
    description="Replace an existing conversation intelligence record with updated data.",
)
async def update_conversation_intelligence_record(
    user_id: str,
    intelligence_id: str,
    request: ConversationIntelligenceRecord,
) -> ConversationIntelligenceRecordResponse:
    """Update and return a conversation intelligence record."""
    decoded_id = parse_path_intelligence_id(intelligence_id)

    # Allow keeping the same intelligence ID while changing sentiment/summary.
    if normalize_intelligence_id(request.intelligence_id) != normalize_intelligence_id(
        decoded_id
    ):
        if conversation_intelligence_engine.intelligence_id_exists(
            user_id,
            request.intelligence_id,
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Intelligence already exists",
            )

    record = conversation_intelligence_engine.update_record(
        user_id,
        decoded_id,
        request,
    )
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Intelligence not found",
        )

    return ConversationIntelligenceRecordResponse.from_record(record)


@conversation_intelligence_router.delete(
    "/conversation_intelligence/{user_id}/{intelligence_id}",
    response_model=ConversationIntelligenceRecordResponse,
    summary="Delete conversation intelligence record",
    description="Delete a conversation intelligence record and return the removed record.",
)
async def delete_conversation_intelligence_record(
    user_id: str,
    intelligence_id: str,
) -> ConversationIntelligenceRecordResponse:
    """Delete a conversation intelligence record and return the deleted item."""
    decoded_id = parse_path_intelligence_id(intelligence_id)
    record = conversation_intelligence_engine.delete_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Intelligence not found",
        )

    return ConversationIntelligenceRecordResponse.from_record(record)
