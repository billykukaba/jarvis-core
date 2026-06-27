"""FastAPI routes for the Cognitive Growth Tracker Engine."""

from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, status

from app.cognitive_growth_tracker.cognitive_growth_tracker_engine import (
    normalize_growth_id,
)
from app.cognitive_growth_tracker.schemas import (
    CognitiveGrowthRecord,
    CognitiveGrowthRecordResponse,
    UserCognitiveGrowthTrackerResponse,
)
from app.services.engine_registry import cognitive_growth_tracker_engine

# Router exposed to FastAPI as cognitive_growth_tracker_router in main.py.
cognitive_growth_tracker_router = APIRouter(
    tags=["Cognitive Growth Tracker Engine"],
)


def parse_path_growth_id(growth_id: str) -> str:
    """Decode URL path growth IDs so spaces work in GET, PUT, and DELETE."""
    return unquote(growth_id.replace("+", " "))


@cognitive_growth_tracker_router.post(
    "/cognitive_growth_tracker/{user_id}",
    response_model=CognitiveGrowthRecordResponse,
    summary="Create cognitive growth record",
    description="Create a new cognitive growth record for the specified user.",
)
async def create_cognitive_growth_record(
    user_id: str,
    request: CognitiveGrowthRecord,
) -> CognitiveGrowthRecordResponse:
    """Create and return a cognitive growth record."""
    if cognitive_growth_tracker_engine.growth_id_exists(user_id, request.growth_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Growth record already exists",
        )

    record = cognitive_growth_tracker_engine.create_record(user_id, request)
    return CognitiveGrowthRecordResponse.from_record(record)


@cognitive_growth_tracker_router.get(
    "/cognitive_growth_tracker/{user_id}",
    response_model=UserCognitiveGrowthTrackerResponse,
    summary="Get all cognitive growth records",
    description="Return all cognitive growth records saved by the specified user.",
)
async def get_cognitive_growth_records(
    user_id: str,
) -> UserCognitiveGrowthTrackerResponse:
    """Return all cognitive growth records for a user."""
    records = cognitive_growth_tracker_engine.get_records(user_id)
    return UserCognitiveGrowthTrackerResponse(
        user_id=user_id,
        cognitive_growth_records=[
            CognitiveGrowthRecordResponse.from_record(record) for record in records
        ],
    )


@cognitive_growth_tracker_router.get(
    "/cognitive_growth_tracker/{user_id}/{growth_id}",
    response_model=CognitiveGrowthRecordResponse,
    summary="Get one cognitive growth record",
    description="Return one cognitive growth record identified by growth ID.",
)
async def get_cognitive_growth_record(
    user_id: str,
    growth_id: str,
) -> CognitiveGrowthRecordResponse:
    """Return a single cognitive growth record by ID."""
    decoded_id = parse_path_growth_id(growth_id)
    record = cognitive_growth_tracker_engine.get_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Growth record not found",
        )

    return CognitiveGrowthRecordResponse.from_record(record)


@cognitive_growth_tracker_router.put(
    "/cognitive_growth_tracker/{user_id}/{growth_id}",
    response_model=CognitiveGrowthRecordResponse,
    status_code=status.HTTP_200_OK,
    summary="Update cognitive growth record",
    description="Replace an existing cognitive growth record with updated data.",
)
async def update_cognitive_growth_record(
    user_id: str,
    growth_id: str,
    request: CognitiveGrowthRecord,
) -> CognitiveGrowthRecordResponse:
    """Update and return a cognitive growth record."""
    decoded_id = parse_path_growth_id(growth_id)

    if normalize_growth_id(request.growth_id) != normalize_growth_id(decoded_id):
        if cognitive_growth_tracker_engine.growth_id_exists(user_id, request.growth_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Growth record already exists",
            )

    record = cognitive_growth_tracker_engine.update_record(
        user_id,
        decoded_id,
        request,
    )
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Growth record not found",
        )

    return CognitiveGrowthRecordResponse.from_record(record)


@cognitive_growth_tracker_router.delete(
    "/cognitive_growth_tracker/{user_id}/{growth_id}",
    response_model=CognitiveGrowthRecordResponse,
    summary="Delete cognitive growth record",
    description="Delete a cognitive growth record and return the removed record.",
)
async def delete_cognitive_growth_record(
    user_id: str,
    growth_id: str,
) -> CognitiveGrowthRecordResponse:
    """Delete a cognitive growth record and return the deleted item."""
    decoded_id = parse_path_growth_id(growth_id)
    record = cognitive_growth_tracker_engine.delete_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Growth record not found",
        )

    return CognitiveGrowthRecordResponse.from_record(record)
