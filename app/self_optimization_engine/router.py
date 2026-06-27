"""FastAPI routes for the Self Optimization Engine.

Tracks and manages performance optimization strategies applied to Jarvis systems
and agents.
"""

from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, status

from app.self_optimization_engine.schemas import (
    SelfOptimizationRecord,
    SelfOptimizationRecordResponse,
    UserSelfOptimizationEngineResponse,
)
from app.self_optimization_engine.self_optimization_engine_engine import (
    normalize_optimization_id,
)
from app.services.engine_registry import self_optimization_engine

# Router exposed to FastAPI as self_optimization_engine_router in main.py.
self_optimization_engine_router = APIRouter(tags=["Self Optimization Engine"])


def parse_path_optimization_id(optimization_id: str) -> str:
    """Decode URL path optimization IDs so spaces work in GET, PUT, and DELETE."""
    return unquote(optimization_id.replace("+", " "))


@self_optimization_engine_router.post(
    "/self_optimization_engine/{user_id}",
    response_model=SelfOptimizationRecordResponse,
    summary="Create optimization record",
    description=(
        "Create a new self optimization record for the specified user. "
        "Tracks and manages performance optimization strategies applied to "
        "Jarvis systems and agents."
    ),
)
async def create_self_optimization_record(
    user_id: str,
    request: SelfOptimizationRecord,
) -> SelfOptimizationRecordResponse:
    """Create and return a self optimization record."""
    if self_optimization_engine.optimization_id_exists(
        user_id,
        request.optimization_id,
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Optimization record already exists",
        )

    record = self_optimization_engine.create_record(user_id, request)
    return SelfOptimizationRecordResponse.from_record(record)


@self_optimization_engine_router.get(
    "/self_optimization_engine/{user_id}",
    response_model=UserSelfOptimizationEngineResponse,
    summary="Get all optimization records",
    description=(
        "Return all self optimization records saved by the specified user. "
        "Tracks and manages performance optimization strategies applied to "
        "Jarvis systems and agents."
    ),
)
async def get_self_optimization_records(
    user_id: str,
) -> UserSelfOptimizationEngineResponse:
    """Return all self optimization records for a user."""
    records = self_optimization_engine.get_records(user_id)
    return UserSelfOptimizationEngineResponse(
        user_id=user_id,
        optimization_records=[
            SelfOptimizationRecordResponse.from_record(record) for record in records
        ],
    )


@self_optimization_engine_router.get(
    "/self_optimization_engine/{user_id}/{optimization_id}",
    response_model=SelfOptimizationRecordResponse,
    summary="Get one optimization record",
    description="Return one self optimization record identified by optimization ID.",
)
async def get_self_optimization_record(
    user_id: str,
    optimization_id: str,
) -> SelfOptimizationRecordResponse:
    """Return a single self optimization record by ID."""
    decoded_id = parse_path_optimization_id(optimization_id)
    record = self_optimization_engine.get_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Optimization record not found",
        )

    return SelfOptimizationRecordResponse.from_record(record)


@self_optimization_engine_router.put(
    "/self_optimization_engine/{user_id}/{optimization_id}",
    response_model=SelfOptimizationRecordResponse,
    status_code=status.HTTP_200_OK,
    summary="Update optimization record",
    description="Replace an existing self optimization record with updated data.",
)
async def update_self_optimization_record(
    user_id: str,
    optimization_id: str,
    request: SelfOptimizationRecord,
) -> SelfOptimizationRecordResponse:
    """Update and return a self optimization record."""
    decoded_id = parse_path_optimization_id(optimization_id)

    if normalize_optimization_id(
        request.optimization_id,
    ) != normalize_optimization_id(decoded_id):
        if self_optimization_engine.optimization_id_exists(
            user_id,
            request.optimization_id,
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Optimization record already exists",
            )

    record = self_optimization_engine.update_record(
        user_id,
        decoded_id,
        request,
    )
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Optimization record not found",
        )

    return SelfOptimizationRecordResponse.from_record(record)


@self_optimization_engine_router.delete(
    "/self_optimization_engine/{user_id}/{optimization_id}",
    response_model=SelfOptimizationRecordResponse,
    summary="Delete optimization record",
    description="Delete a self optimization record and return the removed record.",
)
async def delete_self_optimization_record(
    user_id: str,
    optimization_id: str,
) -> SelfOptimizationRecordResponse:
    """Delete a self optimization record and return the deleted item."""
    decoded_id = parse_path_optimization_id(optimization_id)
    record = self_optimization_engine.delete_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Optimization record not found",
        )

    return SelfOptimizationRecordResponse.from_record(record)
