"""FastAPI routes for the Knowledge Gap Detector Engine (Module 59)."""

from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, status

from app.knowledge_gap_detector.knowledge_gap_detector_engine import normalize_gap_id
from app.knowledge_gap_detector.schemas import (
    KnowledgeGap,
    KnowledgeGapResponse,
    UserKnowledgeGapDetectorResponse,
)
from app.services.engine_registry import knowledge_gap_detector_engine

# Router exposed to FastAPI as knowledge_gap_detector_router in main.py.
knowledge_gap_detector_router = APIRouter(tags=["Knowledge Gap Detector Engine"])


def parse_path_gap_id(gap_id: str) -> str:
    """Decode URL path gap IDs so spaces work in GET, PUT, and DELETE."""
    return unquote(gap_id.replace("+", " "))


@knowledge_gap_detector_router.post(
    "/knowledge_gap_detector/{user_id}",
    response_model=KnowledgeGapResponse,
    summary="Create knowledge gap record",
    description="Create a new knowledge gap record for the specified user.",
)
async def create_knowledge_gap_record(
    user_id: str,
    request: KnowledgeGap,
) -> KnowledgeGapResponse:
    """Create and return a knowledge gap record."""
    if knowledge_gap_detector_engine.gap_id_exists(user_id, request.gap_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Gap already exists",
        )

    record = knowledge_gap_detector_engine.create_record(user_id, request)
    return KnowledgeGapResponse.from_gap(record)


@knowledge_gap_detector_router.get(
    "/knowledge_gap_detector/{user_id}",
    response_model=UserKnowledgeGapDetectorResponse,
    summary="Get all knowledge gap records",
    description="Return all knowledge gap records saved by the specified user.",
)
async def get_knowledge_gap_records(
    user_id: str,
) -> UserKnowledgeGapDetectorResponse:
    """Return all knowledge gap records for a user."""
    records = knowledge_gap_detector_engine.get_records(user_id)
    return UserKnowledgeGapDetectorResponse(
        user_id=user_id,
        knowledge_gaps=[
            KnowledgeGapResponse.from_gap(record) for record in records
        ],
    )


@knowledge_gap_detector_router.get(
    "/knowledge_gap_detector/{user_id}/{gap_id}",
    response_model=KnowledgeGapResponse,
    summary="Get one knowledge gap record",
    description="Return one knowledge gap record identified by gap ID.",
)
async def get_knowledge_gap_record(
    user_id: str,
    gap_id: str,
) -> KnowledgeGapResponse:
    """Return a single knowledge gap record by ID."""
    decoded_id = parse_path_gap_id(gap_id)
    record = knowledge_gap_detector_engine.get_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gap not found",
        )

    return KnowledgeGapResponse.from_gap(record)


@knowledge_gap_detector_router.put(
    "/knowledge_gap_detector/{user_id}/{gap_id}",
    response_model=KnowledgeGapResponse,
    status_code=status.HTTP_200_OK,
    summary="Update knowledge gap record",
    description="Replace an existing knowledge gap record with updated data.",
)
async def update_knowledge_gap_record(
    user_id: str,
    gap_id: str,
    request: KnowledgeGap,
) -> KnowledgeGapResponse:
    """Update and return a knowledge gap record."""
    decoded_id = parse_path_gap_id(gap_id)

    # Allow keeping the same gap ID while changing topic/severity/recommendation.
    if normalize_gap_id(request.gap_id) != normalize_gap_id(decoded_id):
        if knowledge_gap_detector_engine.gap_id_exists(user_id, request.gap_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Gap already exists",
            )

    record = knowledge_gap_detector_engine.update_record(
        user_id,
        decoded_id,
        request,
    )
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gap not found",
        )

    return KnowledgeGapResponse.from_gap(record)


@knowledge_gap_detector_router.delete(
    "/knowledge_gap_detector/{user_id}/{gap_id}",
    response_model=KnowledgeGapResponse,
    summary="Delete knowledge gap record",
    description="Delete a knowledge gap record and return the removed record.",
)
async def delete_knowledge_gap_record(
    user_id: str,
    gap_id: str,
) -> KnowledgeGapResponse:
    """Delete a knowledge gap record and return the deleted item."""
    decoded_id = parse_path_gap_id(gap_id)
    record = knowledge_gap_detector_engine.delete_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gap not found",
        )

    return KnowledgeGapResponse.from_gap(record)
