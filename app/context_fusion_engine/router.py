"""FastAPI routes for the Context Fusion Engine.

Fuses conversation context, memory, goals, emotions and knowledge into a unified
understanding layer for Jarvis.
"""

from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, status

from app.context_fusion_engine.context_fusion_engine_engine import normalize_fusion_id
from app.context_fusion_engine.schemas import (
    ContextFusionRecord,
    ContextFusionRecordResponse,
    UserContextFusionEngineResponse,
)
from app.services.engine_registry import context_fusion_engine

# Router exposed to FastAPI as context_fusion_engine_router in main.py.
context_fusion_engine_router = APIRouter(tags=["Context Fusion Engine"])


def parse_path_fusion_id(fusion_id: str) -> str:
    """Decode URL path fusion IDs so spaces work in GET, PUT, and DELETE."""
    return unquote(fusion_id.replace("+", " "))


@context_fusion_engine_router.post(
    "/context_fusion_engine/{user_id}",
    response_model=ContextFusionRecordResponse,
    summary="Create context fusion record",
    description=(
        "Create a new context fusion record for the specified user. "
        "Fuses conversation context, memory, goals, emotions and knowledge "
        "into a unified understanding layer for Jarvis."
    ),
)
async def create_context_fusion_record(
    user_id: str,
    request: ContextFusionRecord,
) -> ContextFusionRecordResponse:
    """Create and return a context fusion record."""
    if context_fusion_engine.fusion_id_exists(user_id, request.fusion_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Context fusion record already exists",
        )

    record = context_fusion_engine.create_record(user_id, request)
    return ContextFusionRecordResponse.from_record(record)


@context_fusion_engine_router.get(
    "/context_fusion_engine/{user_id}",
    response_model=UserContextFusionEngineResponse,
    summary="Get all context fusion records",
    description=(
        "Return all context fusion records saved by the specified user. "
        "Fuses conversation context, memory, goals, emotions and knowledge "
        "into a unified understanding layer for Jarvis."
    ),
)
async def get_context_fusion_records(
    user_id: str,
) -> UserContextFusionEngineResponse:
    """Return all context fusion records for a user."""
    records = context_fusion_engine.get_records(user_id)
    return UserContextFusionEngineResponse(
        user_id=user_id,
        context_fusion_records=[
            ContextFusionRecordResponse.from_record(record) for record in records
        ],
    )


@context_fusion_engine_router.get(
    "/context_fusion_engine/{user_id}/{fusion_id}",
    response_model=ContextFusionRecordResponse,
    summary="Get one context fusion record",
    description="Return one context fusion record identified by fusion ID.",
)
async def get_context_fusion_record(
    user_id: str,
    fusion_id: str,
) -> ContextFusionRecordResponse:
    """Return a single context fusion record by ID."""
    decoded_id = parse_path_fusion_id(fusion_id)
    record = context_fusion_engine.get_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Context fusion record not found",
        )

    return ContextFusionRecordResponse.from_record(record)


@context_fusion_engine_router.put(
    "/context_fusion_engine/{user_id}/{fusion_id}",
    response_model=ContextFusionRecordResponse,
    status_code=status.HTTP_200_OK,
    summary="Update context fusion record",
    description="Replace an existing context fusion record with updated data.",
)
async def update_context_fusion_record(
    user_id: str,
    fusion_id: str,
    request: ContextFusionRecord,
) -> ContextFusionRecordResponse:
    """Update and return a context fusion record."""
    decoded_id = parse_path_fusion_id(fusion_id)

    if normalize_fusion_id(request.fusion_id) != normalize_fusion_id(decoded_id):
        if context_fusion_engine.fusion_id_exists(user_id, request.fusion_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Context fusion record already exists",
            )

    record = context_fusion_engine.update_record(
        user_id,
        decoded_id,
        request,
    )
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Context fusion record not found",
        )

    return ContextFusionRecordResponse.from_record(record)


@context_fusion_engine_router.delete(
    "/context_fusion_engine/{user_id}/{fusion_id}",
    response_model=ContextFusionRecordResponse,
    summary="Delete context fusion record",
    description="Delete a context fusion record and return the removed record.",
)
async def delete_context_fusion_record(
    user_id: str,
    fusion_id: str,
) -> ContextFusionRecordResponse:
    """Delete a context fusion record and return the deleted item."""
    decoded_id = parse_path_fusion_id(fusion_id)
    record = context_fusion_engine.delete_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Context fusion record not found",
        )

    return ContextFusionRecordResponse.from_record(record)
