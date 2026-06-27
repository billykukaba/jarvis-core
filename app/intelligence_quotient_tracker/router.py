"""FastAPI routes for the Intelligence Quotient Tracker Engine (Module 62)."""

from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, status

from app.intelligence_quotient_tracker.intelligence_quotient_tracker_engine import (
    normalize_iq_id,
)
from app.intelligence_quotient_tracker.schemas import (
    IntelligenceQuotientRecord,
    IntelligenceQuotientRecordResponse,
    UserIntelligenceQuotientTrackerResponse,
)
from app.services.engine_registry import intelligence_quotient_tracker_engine

# Router exposed to FastAPI as intelligence_quotient_tracker_router in main.py.
intelligence_quotient_tracker_router = APIRouter(
    tags=["Intelligence Quotient Tracker Engine"],
)


def parse_path_iq_id(iq_id: str) -> str:
    """Decode URL path IQ IDs so spaces work in GET, PUT, and DELETE."""
    return unquote(iq_id.replace("+", " "))


@intelligence_quotient_tracker_router.post(
    "/intelligence_quotient_tracker/{user_id}",
    response_model=IntelligenceQuotientRecordResponse,
    summary="Create IQ record",
    description="Create a new intelligence quotient record for the specified user.",
)
async def create_intelligence_quotient_record(
    user_id: str,
    request: IntelligenceQuotientRecord,
) -> IntelligenceQuotientRecordResponse:
    """Create and return an IQ record."""
    if intelligence_quotient_tracker_engine.iq_id_exists(user_id, request.iq_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="IQ record already exists",
        )

    record = intelligence_quotient_tracker_engine.create_record(user_id, request)
    return IntelligenceQuotientRecordResponse.from_record(record)


@intelligence_quotient_tracker_router.get(
    "/intelligence_quotient_tracker/{user_id}",
    response_model=UserIntelligenceQuotientTrackerResponse,
    summary="Get all IQ records",
    description="Return all intelligence quotient records saved by the specified user.",
)
async def get_intelligence_quotient_records(
    user_id: str,
) -> UserIntelligenceQuotientTrackerResponse:
    """Return all IQ records for a user."""
    records = intelligence_quotient_tracker_engine.get_records(user_id)
    return UserIntelligenceQuotientTrackerResponse(
        user_id=user_id,
        iq_records=[
            IntelligenceQuotientRecordResponse.from_record(record)
            for record in records
        ],
    )


@intelligence_quotient_tracker_router.get(
    "/intelligence_quotient_tracker/{user_id}/{iq_id}",
    response_model=IntelligenceQuotientRecordResponse,
    summary="Get one IQ record",
    description="Return one intelligence quotient record identified by IQ ID.",
)
async def get_intelligence_quotient_record(
    user_id: str,
    iq_id: str,
) -> IntelligenceQuotientRecordResponse:
    """Return a single IQ record by ID."""
    decoded_id = parse_path_iq_id(iq_id)
    record = intelligence_quotient_tracker_engine.get_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="IQ record not found",
        )

    return IntelligenceQuotientRecordResponse.from_record(record)


@intelligence_quotient_tracker_router.put(
    "/intelligence_quotient_tracker/{user_id}/{iq_id}",
    response_model=IntelligenceQuotientRecordResponse,
    status_code=status.HTTP_200_OK,
    summary="Update IQ record",
    description="Replace an existing intelligence quotient record with updated data.",
)
async def update_intelligence_quotient_record(
    user_id: str,
    iq_id: str,
    request: IntelligenceQuotientRecord,
) -> IntelligenceQuotientRecordResponse:
    """Update and return an IQ record."""
    decoded_id = parse_path_iq_id(iq_id)

    if normalize_iq_id(request.iq_id) != normalize_iq_id(decoded_id):
        if intelligence_quotient_tracker_engine.iq_id_exists(user_id, request.iq_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="IQ record already exists",
            )

    record = intelligence_quotient_tracker_engine.update_record(
        user_id,
        decoded_id,
        request,
    )
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="IQ record not found",
        )

    return IntelligenceQuotientRecordResponse.from_record(record)


@intelligence_quotient_tracker_router.delete(
    "/intelligence_quotient_tracker/{user_id}/{iq_id}",
    response_model=IntelligenceQuotientRecordResponse,
    summary="Delete IQ record",
    description="Delete an intelligence quotient record and return the removed record.",
)
async def delete_intelligence_quotient_record(
    user_id: str,
    iq_id: str,
) -> IntelligenceQuotientRecordResponse:
    """Delete an IQ record and return the deleted item."""
    decoded_id = parse_path_iq_id(iq_id)
    record = intelligence_quotient_tracker_engine.delete_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="IQ record not found",
        )

    return IntelligenceQuotientRecordResponse.from_record(record)
