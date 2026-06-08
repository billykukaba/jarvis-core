"""FastAPI routes for the Education Service."""

from fastapi import APIRouter, HTTPException, status

from app.education.schemas import (
    EducationRecord,
    EducationRecordResponse,
    UserEducationResponse,
)
from app.services.engine_registry import education_service_engine

# Router exposed to FastAPI as education_router in main.py.
education_router = APIRouter(tags=["education"])


@education_router.post(
    "/education/{user_id}",
    response_model=EducationRecordResponse,
    summary="Create education record",
    description="Create a new education record for the specified user.",
)
async def create_education_record(
    user_id: str,
    request: EducationRecord,
) -> EducationRecordResponse:
    """Create and return an education record."""
    if education_service_engine.institution_exists(user_id, request.institution):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Education record for this institution already exists",
        )

    record = education_service_engine.create_record(user_id, request)
    return EducationRecordResponse.from_record(record)


@education_router.get(
    "/education/{user_id}",
    response_model=UserEducationResponse,
    summary="Get all education records",
    description="Return all education records saved by the specified user.",
)
async def get_education_records(user_id: str) -> UserEducationResponse:
    """Return all education records for a user."""
    records = education_service_engine.get_records(user_id)
    return UserEducationResponse(
        user_id=user_id,
        education=[
            EducationRecordResponse.from_record(record) for record in records
        ],
    )


@education_router.get(
    "/education/{user_id}/{institution}",
    response_model=EducationRecordResponse,
    summary="Get one education record",
    description="Return one education record identified by institution.",
)
async def get_education_record(
    user_id: str,
    institution: str,
) -> EducationRecordResponse:
    """Return a single education record by institution."""
    record = education_service_engine.get_record(user_id, institution)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Education record not found",
        )

    return EducationRecordResponse.from_record(record)


@education_router.put(
    "/education/{user_id}/{institution}",
    response_model=EducationRecordResponse,
    summary="Update education record",
    description="Replace an existing education record with updated data.",
)
async def update_education_record(
    user_id: str,
    institution: str,
    request: EducationRecord,
) -> EducationRecordResponse:
    """Update and return an education record."""
    if (
        request.institution.lower() != institution.lower()
        and education_service_engine.institution_exists(user_id, request.institution)
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Education record for this institution already exists",
        )

    record = education_service_engine.update_record(user_id, institution, request)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Education record not found",
        )

    return EducationRecordResponse.from_record(record)


@education_router.delete(
    "/education/{user_id}/{institution}",
    response_model=EducationRecordResponse,
    summary="Delete education record",
    description="Delete an education record and return the removed record.",
)
async def delete_education_record(
    user_id: str,
    institution: str,
) -> EducationRecordResponse:
    """Delete an education record and return the deleted item."""
    record = education_service_engine.delete_record(user_id, institution)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Education record not found",
        )

    return EducationRecordResponse.from_record(record)
