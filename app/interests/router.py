"""FastAPI routes for the Interests Service (Module 59)."""

from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, status

from app.interests.interest_service_engine import normalize_interest
from app.interests.schemas import (
    InterestRecord,
    InterestRecordResponse,
    UserInterestsResponse,
)
from app.services.engine_registry import interest_service_engine

# Router exposed to FastAPI as interests_router in main.py.
interests_router = APIRouter(tags=["interests"])


def parse_path_interest(interest: str) -> str:
    """Decode URL path interest names so spaces work in GET, PUT, and DELETE."""
    return unquote(interest.replace("+", " "))


@interests_router.post(
    "/interests/{user_id}",
    response_model=InterestRecordResponse,
    summary="Create interest record",
    description="Create a new personal interest record for the specified user.",
)
async def create_interest_record(
    user_id: str,
    request: InterestRecord,
) -> InterestRecordResponse:
    """Create and return an interest record."""
    if interest_service_engine.interest_exists(user_id, request.interest):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Interest already exists",
        )

    record = interest_service_engine.create_record(user_id, request)
    return InterestRecordResponse.from_record(record)


@interests_router.get(
    "/interests/{user_id}",
    response_model=UserInterestsResponse,
    summary="Get all interest records",
    description="Return all interest records saved by the specified user.",
)
async def get_interest_records(user_id: str) -> UserInterestsResponse:
    """Return all interest records for a user."""
    records = interest_service_engine.get_records(user_id)
    return UserInterestsResponse(
        user_id=user_id,
        interests=[
            InterestRecordResponse.from_record(record) for record in records
        ],
    )


@interests_router.get(
    "/interests/{user_id}/{interest}",
    response_model=InterestRecordResponse,
    summary="Get one interest record",
    description="Return one interest record identified by interest name.",
)
async def get_interest_record(
    user_id: str,
    interest: str,
) -> InterestRecordResponse:
    """Return a single interest record by name."""
    decoded_interest = parse_path_interest(interest)
    record = interest_service_engine.get_record(user_id, decoded_interest)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interest not found",
        )

    return InterestRecordResponse.from_record(record)


@interests_router.put(
    "/interests/{user_id}/{interest}",
    response_model=InterestRecordResponse,
    status_code=status.HTTP_200_OK,
    summary="Update interest record",
    description="Replace an existing interest record with updated data.",
)
async def update_interest_record(
    user_id: str,
    interest: str,
    request: InterestRecord,
) -> InterestRecordResponse:
    """Update and return an interest record."""
    decoded_interest = parse_path_interest(interest)

    # Allow keeping the same interest while changing level.
    if normalize_interest(request.interest) != normalize_interest(decoded_interest):
        if interest_service_engine.interest_exists(user_id, request.interest):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Interest already exists",
            )

    record = interest_service_engine.update_record(
        user_id,
        decoded_interest,
        request,
    )
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interest not found",
        )

    return InterestRecordResponse.from_record(record)


@interests_router.delete(
    "/interests/{user_id}/{interest}",
    response_model=InterestRecordResponse,
    summary="Delete interest record",
    description="Delete an interest record and return the removed record.",
)
async def delete_interest_record(
    user_id: str,
    interest: str,
) -> InterestRecordResponse:
    """Delete an interest record and return the deleted item."""
    decoded_interest = parse_path_interest(interest)
    record = interest_service_engine.delete_record(user_id, decoded_interest)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interest not found",
        )

    return InterestRecordResponse.from_record(record)
