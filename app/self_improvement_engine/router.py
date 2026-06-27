"""FastAPI routes for the Self Improvement Engine.

Continuously analyzes Jarvis performance and stores improvement opportunities
for autonomous evolution.
"""

from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, status

from app.self_improvement_engine.schemas import (
    SelfImprovementRecord,
    SelfImprovementRecordResponse,
    UserSelfImprovementEngineResponse,
)
from app.self_improvement_engine.self_improvement_engine_engine import (
    normalize_improvement_id,
)
from app.services.engine_registry import self_improvement_engine

# Router exposed to FastAPI as self_improvement_engine_router in main.py.
self_improvement_engine_router = APIRouter(tags=["Self Improvement Engine"])


def parse_path_improvement_id(improvement_id: str) -> str:
    """Decode URL path improvement IDs so spaces work in GET, PUT, and DELETE."""
    return unquote(improvement_id.replace("+", " "))


@self_improvement_engine_router.post(
    "/self_improvement_engine/{user_id}",
    response_model=SelfImprovementRecordResponse,
    summary="Create improvement record",
    description=(
        "Create a new self improvement record for the specified user. "
        "Continuously analyzes Jarvis performance and stores improvement "
        "opportunities for autonomous evolution."
    ),
)
async def create_self_improvement_record(
    user_id: str,
    request: SelfImprovementRecord,
) -> SelfImprovementRecordResponse:
    """Create and return a self improvement record."""
    if self_improvement_engine.improvement_id_exists(user_id, request.improvement_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Improvement record already exists",
        )

    record = self_improvement_engine.create_record(user_id, request)
    return SelfImprovementRecordResponse.from_record(record)


@self_improvement_engine_router.get(
    "/self_improvement_engine/{user_id}",
    response_model=UserSelfImprovementEngineResponse,
    summary="Get all improvement records",
    description=(
        "Return all self improvement records saved by the specified user. "
        "Continuously analyzes Jarvis performance and stores improvement "
        "opportunities for autonomous evolution."
    ),
)
async def get_self_improvement_records(
    user_id: str,
) -> UserSelfImprovementEngineResponse:
    """Return all self improvement records for a user."""
    records = self_improvement_engine.get_records(user_id)
    return UserSelfImprovementEngineResponse(
        user_id=user_id,
        improvement_records=[
            SelfImprovementRecordResponse.from_record(record) for record in records
        ],
    )


@self_improvement_engine_router.get(
    "/self_improvement_engine/{user_id}/{improvement_id}",
    response_model=SelfImprovementRecordResponse,
    summary="Get one improvement record",
    description="Return one self improvement record identified by improvement ID.",
)
async def get_self_improvement_record(
    user_id: str,
    improvement_id: str,
) -> SelfImprovementRecordResponse:
    """Return a single self improvement record by ID."""
    decoded_id = parse_path_improvement_id(improvement_id)
    record = self_improvement_engine.get_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Improvement record not found",
        )

    return SelfImprovementRecordResponse.from_record(record)


@self_improvement_engine_router.put(
    "/self_improvement_engine/{user_id}/{improvement_id}",
    response_model=SelfImprovementRecordResponse,
    status_code=status.HTTP_200_OK,
    summary="Update improvement record",
    description="Replace an existing self improvement record with updated data.",
)
async def update_self_improvement_record(
    user_id: str,
    improvement_id: str,
    request: SelfImprovementRecord,
) -> SelfImprovementRecordResponse:
    """Update and return a self improvement record."""
    decoded_id = parse_path_improvement_id(improvement_id)

    if normalize_improvement_id(request.improvement_id) != normalize_improvement_id(
        decoded_id,
    ):
        if self_improvement_engine.improvement_id_exists(user_id, request.improvement_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Improvement record already exists",
            )

    record = self_improvement_engine.update_record(
        user_id,
        decoded_id,
        request,
    )
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Improvement record not found",
        )

    return SelfImprovementRecordResponse.from_record(record)


@self_improvement_engine_router.delete(
    "/self_improvement_engine/{user_id}/{improvement_id}",
    response_model=SelfImprovementRecordResponse,
    summary="Delete improvement record",
    description="Delete a self improvement record and return the removed record.",
)
async def delete_self_improvement_record(
    user_id: str,
    improvement_id: str,
) -> SelfImprovementRecordResponse:
    """Delete a self improvement record and return the deleted item."""
    decoded_id = parse_path_improvement_id(improvement_id)
    record = self_improvement_engine.delete_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Improvement record not found",
        )

    return SelfImprovementRecordResponse.from_record(record)
