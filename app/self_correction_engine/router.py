"""FastAPI routes for the Self Correction Engine.

Tracks and manages Jarvis self-corrections after reasoning errors, failed actions,
inaccurate outputs or system mistakes.
"""

from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, status

from app.self_correction_engine.schemas import (
    SelfCorrectionRecord,
    SelfCorrectionRecordResponse,
    UserSelfCorrectionEngineResponse,
)
from app.self_correction_engine.self_correction_engine_engine import (
    normalize_correction_id,
)
from app.services.engine_registry import self_correction_engine

# Router exposed to FastAPI as self_correction_engine_router in main.py.
self_correction_engine_router = APIRouter(tags=["Self Correction Engine"])


def parse_path_correction_id(correction_id: str) -> str:
    """Decode URL path correction IDs so spaces work in GET, PUT, and DELETE."""
    return unquote(correction_id.replace("+", " "))


@self_correction_engine_router.post(
    "/self_correction_engine/{user_id}",
    response_model=SelfCorrectionRecordResponse,
    summary="Create correction record",
    description=(
        "Create a new self correction record for the specified user. "
        "Tracks and manages Jarvis self-corrections after reasoning errors, "
        "failed actions, inaccurate outputs or system mistakes."
    ),
)
async def create_self_correction_record(
    user_id: str,
    request: SelfCorrectionRecord,
) -> SelfCorrectionRecordResponse:
    """Create and return a self correction record."""
    if self_correction_engine.correction_id_exists(user_id, request.correction_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Correction record already exists",
        )

    record = self_correction_engine.create_record(user_id, request)
    return SelfCorrectionRecordResponse.from_record(record)


@self_correction_engine_router.get(
    "/self_correction_engine/{user_id}",
    response_model=UserSelfCorrectionEngineResponse,
    summary="Get all correction records",
    description=(
        "Return all self correction records saved by the specified user. "
        "Tracks and manages Jarvis self-corrections after reasoning errors, "
        "failed actions, inaccurate outputs or system mistakes."
    ),
)
async def get_self_correction_records(
    user_id: str,
) -> UserSelfCorrectionEngineResponse:
    """Return all self correction records for a user."""
    records = self_correction_engine.get_records(user_id)
    return UserSelfCorrectionEngineResponse(
        user_id=user_id,
        correction_records=[
            SelfCorrectionRecordResponse.from_record(record) for record in records
        ],
    )


@self_correction_engine_router.get(
    "/self_correction_engine/{user_id}/{correction_id}",
    response_model=SelfCorrectionRecordResponse,
    summary="Get one correction record",
    description="Return one self correction record identified by correction ID.",
)
async def get_self_correction_record(
    user_id: str,
    correction_id: str,
) -> SelfCorrectionRecordResponse:
    """Return a single self correction record by ID."""
    decoded_id = parse_path_correction_id(correction_id)
    record = self_correction_engine.get_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Correction record not found",
        )

    return SelfCorrectionRecordResponse.from_record(record)


@self_correction_engine_router.put(
    "/self_correction_engine/{user_id}/{correction_id}",
    response_model=SelfCorrectionRecordResponse,
    status_code=status.HTTP_200_OK,
    summary="Update correction record",
    description="Replace an existing self correction record with updated data.",
)
async def update_self_correction_record(
    user_id: str,
    correction_id: str,
    request: SelfCorrectionRecord,
) -> SelfCorrectionRecordResponse:
    """Update and return a self correction record."""
    decoded_id = parse_path_correction_id(correction_id)

    if normalize_correction_id(request.correction_id) != normalize_correction_id(
        decoded_id,
    ):
        if self_correction_engine.correction_id_exists(user_id, request.correction_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Correction record already exists",
            )

    record = self_correction_engine.update_record(
        user_id,
        decoded_id,
        request,
    )
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Correction record not found",
        )

    return SelfCorrectionRecordResponse.from_record(record)


@self_correction_engine_router.delete(
    "/self_correction_engine/{user_id}/{correction_id}",
    response_model=SelfCorrectionRecordResponse,
    summary="Delete correction record",
    description="Delete a self correction record and return the removed record.",
)
async def delete_self_correction_record(
    user_id: str,
    correction_id: str,
) -> SelfCorrectionRecordResponse:
    """Delete a self correction record and return the deleted item."""
    decoded_id = parse_path_correction_id(correction_id)
    record = self_correction_engine.delete_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Correction record not found",
        )

    return SelfCorrectionRecordResponse.from_record(record)
