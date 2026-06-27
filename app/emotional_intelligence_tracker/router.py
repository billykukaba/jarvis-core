"""FastAPI routes for the Emotional Intelligence Tracker Engine (Module 63)."""

from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, status

from app.emotional_intelligence_tracker.emotional_intelligence_tracker_engine import (
    normalize_eq_id,
)
from app.emotional_intelligence_tracker.schemas import (
    EmotionalIntelligenceRecord,
    EmotionalIntelligenceRecordResponse,
    UserEmotionalIntelligenceTrackerResponse,
)
from app.services.engine_registry import emotional_intelligence_tracker_engine

# Router exposed to FastAPI as emotional_intelligence_tracker_router in main.py.
emotional_intelligence_tracker_router = APIRouter(
    tags=["Emotional Intelligence Tracker Engine"],
)


def parse_path_eq_id(eq_id: str) -> str:
    """Decode URL path EQ IDs so spaces work in GET, PUT, and DELETE."""
    return unquote(eq_id.replace("+", " "))


@emotional_intelligence_tracker_router.post(
    "/emotional_intelligence_tracker/{user_id}",
    response_model=EmotionalIntelligenceRecordResponse,
    summary="Create EQ record",
    description="Create a new emotional intelligence record for the specified user.",
)
async def create_emotional_intelligence_record(
    user_id: str,
    request: EmotionalIntelligenceRecord,
) -> EmotionalIntelligenceRecordResponse:
    """Create and return an EQ record."""
    if emotional_intelligence_tracker_engine.eq_id_exists(user_id, request.eq_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="EQ record already exists",
        )

    record = emotional_intelligence_tracker_engine.create_record(user_id, request)
    return EmotionalIntelligenceRecordResponse.from_record(record)


@emotional_intelligence_tracker_router.get(
    "/emotional_intelligence_tracker/{user_id}",
    response_model=UserEmotionalIntelligenceTrackerResponse,
    summary="Get all EQ records",
    description="Return all emotional intelligence records saved by the specified user.",
)
async def get_emotional_intelligence_records(
    user_id: str,
) -> UserEmotionalIntelligenceTrackerResponse:
    """Return all EQ records for a user."""
    records = emotional_intelligence_tracker_engine.get_records(user_id)
    return UserEmotionalIntelligenceTrackerResponse(
        user_id=user_id,
        eq_records=[
            EmotionalIntelligenceRecordResponse.from_record(record)
            for record in records
        ],
    )


@emotional_intelligence_tracker_router.get(
    "/emotional_intelligence_tracker/{user_id}/{eq_id}",
    response_model=EmotionalIntelligenceRecordResponse,
    summary="Get one EQ record",
    description="Return one emotional intelligence record identified by EQ ID.",
)
async def get_emotional_intelligence_record(
    user_id: str,
    eq_id: str,
) -> EmotionalIntelligenceRecordResponse:
    """Return a single EQ record by ID."""
    decoded_id = parse_path_eq_id(eq_id)
    record = emotional_intelligence_tracker_engine.get_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="EQ record not found",
        )

    return EmotionalIntelligenceRecordResponse.from_record(record)


@emotional_intelligence_tracker_router.put(
    "/emotional_intelligence_tracker/{user_id}/{eq_id}",
    response_model=EmotionalIntelligenceRecordResponse,
    status_code=status.HTTP_200_OK,
    summary="Update EQ record",
    description="Replace an existing emotional intelligence record with updated data.",
)
async def update_emotional_intelligence_record(
    user_id: str,
    eq_id: str,
    request: EmotionalIntelligenceRecord,
) -> EmotionalIntelligenceRecordResponse:
    """Update and return an EQ record."""
    decoded_id = parse_path_eq_id(eq_id)

    if normalize_eq_id(request.eq_id) != normalize_eq_id(decoded_id):
        if emotional_intelligence_tracker_engine.eq_id_exists(user_id, request.eq_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="EQ record already exists",
            )

    record = emotional_intelligence_tracker_engine.update_record(
        user_id,
        decoded_id,
        request,
    )
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="EQ record not found",
        )

    return EmotionalIntelligenceRecordResponse.from_record(record)


@emotional_intelligence_tracker_router.delete(
    "/emotional_intelligence_tracker/{user_id}/{eq_id}",
    response_model=EmotionalIntelligenceRecordResponse,
    summary="Delete EQ record",
    description="Delete an emotional intelligence record and return the removed record.",
)
async def delete_emotional_intelligence_record(
    user_id: str,
    eq_id: str,
) -> EmotionalIntelligenceRecordResponse:
    """Delete an EQ record and return the deleted item."""
    decoded_id = parse_path_eq_id(eq_id)
    record = emotional_intelligence_tracker_engine.delete_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="EQ record not found",
        )

    return EmotionalIntelligenceRecordResponse.from_record(record)
