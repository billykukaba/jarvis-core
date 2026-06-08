"""FastAPI routes for the Licenses Service (Module 57)."""

from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, status

from app.licenses.license_service_engine import normalize_name
from app.licenses.schemas import (
    LicenseRecord,
    LicenseRecordResponse,
    UserLicensesResponse,
)
from app.services.engine_registry import license_service_engine

# Router exposed to FastAPI as licenses_router in main.py.
licenses_router = APIRouter(tags=["licenses"])


def parse_path_name(name: str) -> str:
    """Decode URL path names so spaces work in GET, PUT, and DELETE."""
    return unquote(name.replace("+", " "))


@licenses_router.post(
    "/licenses/{user_id}",
    response_model=LicenseRecordResponse,
    summary="Create license record",
    description="Create a new professional license record for the specified user.",
)
async def create_license_record(
    user_id: str,
    request: LicenseRecord,
) -> LicenseRecordResponse:
    """Create and return a license record."""
    if license_service_engine.name_exists(user_id, request.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="License already exists",
        )

    record = license_service_engine.create_record(user_id, request)
    return LicenseRecordResponse.from_record(record)


@licenses_router.get(
    "/licenses/{user_id}",
    response_model=UserLicensesResponse,
    summary="Get all license records",
    description="Return all license records saved by the specified user.",
)
async def get_license_records(user_id: str) -> UserLicensesResponse:
    """Return all license records for a user."""
    records = license_service_engine.get_records(user_id)
    return UserLicensesResponse(
        user_id=user_id,
        licenses=[LicenseRecordResponse.from_record(record) for record in records],
    )


@licenses_router.get(
    "/licenses/{user_id}/{name}",
    response_model=LicenseRecordResponse,
    summary="Get one license record",
    description="Return one license record identified by name.",
)
async def get_license_record(user_id: str, name: str) -> LicenseRecordResponse:
    """Return a single license record by name."""
    decoded_name = parse_path_name(name)
    record = license_service_engine.get_record(user_id, decoded_name)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="License not found",
        )

    return LicenseRecordResponse.from_record(record)


@licenses_router.put(
    "/licenses/{user_id}/{name}",
    response_model=LicenseRecordResponse,
    status_code=status.HTTP_200_OK,
    summary="Update license record",
    description="Replace an existing license record with updated data.",
)
async def update_license_record(
    user_id: str,
    name: str,
    request: LicenseRecord,
) -> LicenseRecordResponse:
    """Update and return a license record."""
    decoded_name = parse_path_name(name)

    # Allow keeping the same name while changing issuer/year.
    if normalize_name(request.name) != normalize_name(decoded_name):
        if license_service_engine.name_exists(user_id, request.name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="License already exists",
            )

    record = license_service_engine.update_record(user_id, decoded_name, request)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="License not found",
        )

    return LicenseRecordResponse.from_record(record)


@licenses_router.delete(
    "/licenses/{user_id}/{name}",
    response_model=LicenseRecordResponse,
    summary="Delete license record",
    description="Delete a license record and return the removed record.",
)
async def delete_license_record(user_id: str, name: str) -> LicenseRecordResponse:
    """Delete a license record and return the deleted item."""
    decoded_name = parse_path_name(name)
    record = license_service_engine.delete_record(user_id, decoded_name)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="License not found",
        )

    return LicenseRecordResponse.from_record(record)
