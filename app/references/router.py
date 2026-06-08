"""FastAPI routes for the References Service (Module 55)."""

from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, status

from app.references.reference_service_engine import normalize_name
from app.references.schemas import (
    ReferenceRecord,
    ReferenceRecordResponse,
    UserReferencesResponse,
)
from app.services.engine_registry import reference_service_engine

# Router exposed to FastAPI as references_router in main.py.
references_router = APIRouter(tags=["references"])


def parse_path_name(name: str) -> str:
    """Decode URL path names so spaces work in GET, PUT, and DELETE."""
    return unquote(name.replace("+", " "))


@references_router.post(
    "/references/{user_id}",
    response_model=ReferenceRecordResponse,
    summary="Create reference record",
    description="Create a new professional reference record for the specified user.",
)
async def create_reference_record(
    user_id: str,
    request: ReferenceRecord,
) -> ReferenceRecordResponse:
    """Create and return a reference record."""
    if reference_service_engine.name_exists(user_id, request.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reference already exists",
        )

    record = reference_service_engine.create_record(user_id, request)
    return ReferenceRecordResponse.from_record(record)


@references_router.get(
    "/references/{user_id}",
    response_model=UserReferencesResponse,
    summary="Get all reference records",
    description="Return all reference records saved by the specified user.",
)
async def get_reference_records(user_id: str) -> UserReferencesResponse:
    """Return all reference records for a user."""
    records = reference_service_engine.get_records(user_id)
    return UserReferencesResponse(
        user_id=user_id,
        references=[
            ReferenceRecordResponse.from_record(record) for record in records
        ],
    )


@references_router.get(
    "/references/{user_id}/{name}",
    response_model=ReferenceRecordResponse,
    summary="Get one reference record",
    description="Return one reference record identified by name.",
)
async def get_reference_record(
    user_id: str,
    name: str,
) -> ReferenceRecordResponse:
    """Return a single reference record by name."""
    decoded_name = parse_path_name(name)
    record = reference_service_engine.get_record(user_id, decoded_name)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reference not found",
        )

    return ReferenceRecordResponse.from_record(record)


@references_router.put(
    "/references/{user_id}/{name}",
    response_model=ReferenceRecordResponse,
    status_code=status.HTTP_200_OK,
    summary="Update reference record",
    description="Replace an existing reference record with updated data.",
)
async def update_reference_record(
    user_id: str,
    name: str,
    request: ReferenceRecord,
) -> ReferenceRecordResponse:
    """Update and return a reference record."""
    decoded_name = parse_path_name(name)

    # Allow keeping the same name while changing title/organization/email.
    if normalize_name(request.name) != normalize_name(decoded_name):
        if reference_service_engine.name_exists(user_id, request.name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Reference already exists",
            )

    record = reference_service_engine.update_record(
        user_id,
        decoded_name,
        request,
    )
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reference not found",
        )

    return ReferenceRecordResponse.from_record(record)


@references_router.delete(
    "/references/{user_id}/{name}",
    response_model=ReferenceRecordResponse,
    summary="Delete reference record",
    description="Delete a reference record and return the removed record.",
)
async def delete_reference_record(
    user_id: str,
    name: str,
) -> ReferenceRecordResponse:
    """Delete a reference record and return the deleted item."""
    decoded_name = parse_path_name(name)
    record = reference_service_engine.delete_record(user_id, decoded_name)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reference not found",
        )

    return ReferenceRecordResponse.from_record(record)
