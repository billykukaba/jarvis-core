"""FastAPI routes for the Reflection Engine."""

from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, status

from app.reflection_engine.reflection_engine import normalize_reflection_id
from app.reflection_engine.schemas import (
    ReflectionRecord,
    ReflectionRecordResponse,
    UserReflectionEngineResponse,
)
from app.services.engine_registry import reflection_engine

# Router exposed to FastAPI as reflection_engine_router in main.py.
reflection_engine_router = APIRouter(tags=["reflection_engine"])


def parse_path_reflection_id(reflection_id: str) -> str:
    """Decode URL path reflection IDs so spaces work in GET, PUT, and DELETE."""
    return unquote(reflection_id.replace("+", " "))


@reflection_engine_router.post(
    "/reflection_engine/{user_id}",
    response_model=ReflectionRecordResponse,
    summary="Create reflection record",
    description="Create a new self-reflection record for the specified user.",
)
async def create_reflection_record(
    user_id: str,
    request: ReflectionRecord,
) -> ReflectionRecordResponse:
    """Create and return a reflection record."""
    if reflection_engine.reflection_id_exists(user_id, request.reflection_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reflection already exists",
        )

    record = reflection_engine.create_record(user_id, request)
    return ReflectionRecordResponse.from_record(record)


@reflection_engine_router.get(
    "/reflection_engine/{user_id}",
    response_model=UserReflectionEngineResponse,
    summary="Get all reflection records",
    description="Return all self-reflection records saved by the specified user.",
)
async def get_reflection_records(user_id: str) -> UserReflectionEngineResponse:
    """Return all reflection records for a user."""
    records = reflection_engine.get_records(user_id)
    return UserReflectionEngineResponse(
        user_id=user_id,
        reflections=[
            ReflectionRecordResponse.from_record(record) for record in records
        ],
    )


@reflection_engine_router.get(
    "/reflection_engine/{user_id}/{reflection_id}",
    response_model=ReflectionRecordResponse,
    summary="Get one reflection record",
    description="Return one self-reflection record identified by reflection ID.",
)
async def get_reflection_record(
    user_id: str,
    reflection_id: str,
) -> ReflectionRecordResponse:
    """Return a single reflection record by ID."""
    decoded_id = parse_path_reflection_id(reflection_id)
    record = reflection_engine.get_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reflection not found",
        )

    return ReflectionRecordResponse.from_record(record)


@reflection_engine_router.put(
    "/reflection_engine/{user_id}/{reflection_id}",
    response_model=ReflectionRecordResponse,
    status_code=status.HTTP_200_OK,
    summary="Update reflection record",
    description="Replace an existing self-reflection record with updated data.",
)
async def update_reflection_record(
    user_id: str,
    reflection_id: str,
    request: ReflectionRecord,
) -> ReflectionRecordResponse:
    """Update and return a reflection record."""
    decoded_id = parse_path_reflection_id(reflection_id)

    # Allow keeping the same reflection ID while changing topic/reflection/score.
    if normalize_reflection_id(request.reflection_id) != normalize_reflection_id(
        decoded_id
    ):
        if reflection_engine.reflection_id_exists(user_id, request.reflection_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Reflection already exists",
            )

    record = reflection_engine.update_record(user_id, decoded_id, request)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reflection not found",
        )

    return ReflectionRecordResponse.from_record(record)


@reflection_engine_router.delete(
    "/reflection_engine/{user_id}/{reflection_id}",
    response_model=ReflectionRecordResponse,
    summary="Delete reflection record",
    description="Delete a self-reflection record and return the removed record.",
)
async def delete_reflection_record(
    user_id: str,
    reflection_id: str,
) -> ReflectionRecordResponse:
    """Delete a reflection record and return the deleted item."""
    decoded_id = parse_path_reflection_id(reflection_id)
    record = reflection_engine.delete_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reflection not found",
        )

    return ReflectionRecordResponse.from_record(record)
