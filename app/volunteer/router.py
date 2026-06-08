"""FastAPI routes for the Volunteer Service (Module 52)."""

from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, status

from app.services.engine_registry import volunteer_service_engine
from app.volunteer.schemas import (
    UserVolunteerResponse,
    VolunteerRecord,
    VolunteerRecordResponse,
)
from app.volunteer.volunteer_service_engine import normalize_organization

# Router exposed to FastAPI as volunteer_router in main.py.
volunteer_router = APIRouter(tags=["volunteer"])


def parse_path_organization(organization: str) -> str:
    """Decode URL path organization names so spaces work in GET, PUT, and DELETE."""
    return unquote(organization.replace("+", " "))


@volunteer_router.post(
    "/volunteer/{user_id}",
    response_model=VolunteerRecordResponse,
    summary="Create volunteer record",
    description="Create a new volunteer record for the specified user.",
)
async def create_volunteer_record(
    user_id: str,
    request: VolunteerRecord,
) -> VolunteerRecordResponse:
    """Create and return a volunteer record."""
    if volunteer_service_engine.organization_exists(user_id, request.organization):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Volunteer record already exists",
        )

    record = volunteer_service_engine.create_record(user_id, request)
    return VolunteerRecordResponse.from_record(record)


@volunteer_router.get(
    "/volunteer/{user_id}",
    response_model=UserVolunteerResponse,
    summary="Get all volunteer records",
    description="Return all volunteer records saved by the specified user.",
)
async def get_volunteer_records(user_id: str) -> UserVolunteerResponse:
    """Return all volunteer records for a user."""
    records = volunteer_service_engine.get_records(user_id)
    return UserVolunteerResponse(
        user_id=user_id,
        volunteer=[
            VolunteerRecordResponse.from_record(record) for record in records
        ],
    )


@volunteer_router.get(
    "/volunteer/{user_id}/{organization}",
    response_model=VolunteerRecordResponse,
    summary="Get one volunteer record",
    description="Return one volunteer record identified by organization.",
)
async def get_volunteer_record(
    user_id: str,
    organization: str,
) -> VolunteerRecordResponse:
    """Return a single volunteer record by organization."""
    decoded_organization = parse_path_organization(organization)
    record = volunteer_service_engine.get_record(user_id, decoded_organization)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Volunteer record not found",
        )

    return VolunteerRecordResponse.from_record(record)


@volunteer_router.put(
    "/volunteer/{user_id}/{organization}",
    response_model=VolunteerRecordResponse,
    status_code=status.HTTP_200_OK,
    summary="Update volunteer record",
    description="Replace an existing volunteer record with updated data.",
)
async def update_volunteer_record(
    user_id: str,
    organization: str,
    request: VolunteerRecord,
) -> VolunteerRecordResponse:
    """Update and return a volunteer record."""
    decoded_organization = parse_path_organization(organization)

    # Allow keeping the same organization while changing role/year.
    if normalize_organization(request.organization) != normalize_organization(
        decoded_organization
    ):
        if volunteer_service_engine.organization_exists(user_id, request.organization):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Volunteer record already exists",
            )

    record = volunteer_service_engine.update_record(
        user_id,
        decoded_organization,
        request,
    )
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Volunteer record not found",
        )

    return VolunteerRecordResponse.from_record(record)


@volunteer_router.delete(
    "/volunteer/{user_id}/{organization}",
    response_model=VolunteerRecordResponse,
    summary="Delete volunteer record",
    description="Delete a volunteer record and return the removed record.",
)
async def delete_volunteer_record(
    user_id: str,
    organization: str,
) -> VolunteerRecordResponse:
    """Delete a volunteer record and return the deleted item."""
    decoded_organization = parse_path_organization(organization)
    record = volunteer_service_engine.delete_record(user_id, decoded_organization)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Volunteer record not found",
        )

    return VolunteerRecordResponse.from_record(record)
