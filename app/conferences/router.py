"""FastAPI routes for the Conferences Service (Module 54)."""

from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, status

from app.conferences.conference_service_engine import normalize_title
from app.conferences.schemas import (
    ConferenceRecord,
    ConferenceRecordResponse,
    UserConferencesResponse,
)
from app.services.engine_registry import conference_service_engine

# Router exposed to FastAPI as conferences_router in main.py.
conferences_router = APIRouter(tags=["conferences"])


def parse_path_title(title: str) -> str:
    """Decode URL path titles so spaces work in GET, PUT, and DELETE."""
    return unquote(title.replace("+", " "))


@conferences_router.post(
    "/conferences/{user_id}",
    response_model=ConferenceRecordResponse,
    summary="Create conference record",
    description="Create a new conference record for the specified user.",
)
async def create_conference_record(
    user_id: str,
    request: ConferenceRecord,
) -> ConferenceRecordResponse:
    """Create and return a conference record."""
    if conference_service_engine.title_exists(user_id, request.title):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Conference record already exists",
        )

    record = conference_service_engine.create_record(user_id, request)
    return ConferenceRecordResponse.from_record(record)


@conferences_router.get(
    "/conferences/{user_id}",
    response_model=UserConferencesResponse,
    summary="Get all conference records",
    description="Return all conference records saved by the specified user.",
)
async def get_conference_records(user_id: str) -> UserConferencesResponse:
    """Return all conference records for a user."""
    records = conference_service_engine.get_records(user_id)
    return UserConferencesResponse(
        user_id=user_id,
        conferences=[
            ConferenceRecordResponse.from_record(record) for record in records
        ],
    )


@conferences_router.get(
    "/conferences/{user_id}/{title}",
    response_model=ConferenceRecordResponse,
    summary="Get one conference record",
    description="Return one conference record identified by title.",
)
async def get_conference_record(
    user_id: str,
    title: str,
) -> ConferenceRecordResponse:
    """Return a single conference record by title."""
    decoded_title = parse_path_title(title)
    record = conference_service_engine.get_record(user_id, decoded_title)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conference record not found",
        )

    return ConferenceRecordResponse.from_record(record)


@conferences_router.put(
    "/conferences/{user_id}/{title}",
    response_model=ConferenceRecordResponse,
    status_code=status.HTTP_200_OK,
    summary="Update conference record",
    description="Replace an existing conference record with updated data.",
)
async def update_conference_record(
    user_id: str,
    title: str,
    request: ConferenceRecord,
) -> ConferenceRecordResponse:
    """Update and return a conference record."""
    decoded_title = parse_path_title(title)

    # Allow keeping the same title while changing event/year.
    if normalize_title(request.title) != normalize_title(decoded_title):
        if conference_service_engine.title_exists(user_id, request.title):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Conference record already exists",
            )

    record = conference_service_engine.update_record(
        user_id,
        decoded_title,
        request,
    )
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conference record not found",
        )

    return ConferenceRecordResponse.from_record(record)


@conferences_router.delete(
    "/conferences/{user_id}/{title}",
    response_model=ConferenceRecordResponse,
    summary="Delete conference record",
    description="Delete a conference record and return the removed record.",
)
async def delete_conference_record(
    user_id: str,
    title: str,
) -> ConferenceRecordResponse:
    """Delete a conference record and return the deleted item."""
    decoded_title = parse_path_title(title)
    record = conference_service_engine.delete_record(user_id, decoded_title)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conference record not found",
        )

    return ConferenceRecordResponse.from_record(record)
