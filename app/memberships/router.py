"""FastAPI routes for the Memberships Service (Module 56)."""

from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, status

from app.memberships.membership_service_engine import normalize_organization
from app.memberships.schemas import (
    MembershipRecord,
    MembershipRecordResponse,
    UserMembershipsResponse,
)
from app.services.engine_registry import membership_service_engine

# Router exposed to FastAPI as memberships_router in main.py.
memberships_router = APIRouter(tags=["memberships"])


def parse_path_organization(organization: str) -> str:
    """Decode URL path organization names so spaces work in GET, PUT, and DELETE."""
    return unquote(organization.replace("+", " "))


@memberships_router.post(
    "/memberships/{user_id}",
    response_model=MembershipRecordResponse,
    summary="Create membership record",
    description="Create a new professional membership record for the specified user.",
)
async def create_membership_record(
    user_id: str,
    request: MembershipRecord,
) -> MembershipRecordResponse:
    """Create and return a membership record."""
    if membership_service_engine.organization_exists(user_id, request.organization):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Membership already exists",
        )

    record = membership_service_engine.create_record(user_id, request)
    return MembershipRecordResponse.from_record(record)


@memberships_router.get(
    "/memberships/{user_id}",
    response_model=UserMembershipsResponse,
    summary="Get all membership records",
    description="Return all membership records saved by the specified user.",
)
async def get_membership_records(user_id: str) -> UserMembershipsResponse:
    """Return all membership records for a user."""
    records = membership_service_engine.get_records(user_id)
    return UserMembershipsResponse(
        user_id=user_id,
        memberships=[
            MembershipRecordResponse.from_record(record) for record in records
        ],
    )


@memberships_router.get(
    "/memberships/{user_id}/{organization}",
    response_model=MembershipRecordResponse,
    summary="Get one membership record",
    description="Return one membership record identified by organization.",
)
async def get_membership_record(
    user_id: str,
    organization: str,
) -> MembershipRecordResponse:
    """Return a single membership record by organization."""
    decoded_organization = parse_path_organization(organization)
    record = membership_service_engine.get_record(user_id, decoded_organization)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Membership not found",
        )

    return MembershipRecordResponse.from_record(record)


@memberships_router.put(
    "/memberships/{user_id}/{organization}",
    response_model=MembershipRecordResponse,
    status_code=status.HTTP_200_OK,
    summary="Update membership record",
    description="Replace an existing membership record with updated data.",
)
async def update_membership_record(
    user_id: str,
    organization: str,
    request: MembershipRecord,
) -> MembershipRecordResponse:
    """Update and return a membership record."""
    decoded_organization = parse_path_organization(organization)

    # Allow keeping the same organization while changing role/year.
    if normalize_organization(request.organization) != normalize_organization(
        decoded_organization
    ):
        if membership_service_engine.organization_exists(user_id, request.organization):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Membership already exists",
            )

    record = membership_service_engine.update_record(
        user_id,
        decoded_organization,
        request,
    )
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Membership not found",
        )

    return MembershipRecordResponse.from_record(record)


@memberships_router.delete(
    "/memberships/{user_id}/{organization}",
    response_model=MembershipRecordResponse,
    summary="Delete membership record",
    description="Delete a membership record and return the removed record.",
)
async def delete_membership_record(
    user_id: str,
    organization: str,
) -> MembershipRecordResponse:
    """Delete a membership record and return the deleted item."""
    decoded_organization = parse_path_organization(organization)
    record = membership_service_engine.delete_record(user_id, decoded_organization)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Membership not found",
        )

    return MembershipRecordResponse.from_record(record)
