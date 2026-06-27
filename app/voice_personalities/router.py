"""FastAPI routes for the Voice Personality Engine (Module 65)."""

from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, status

from app.voice_personalities.schemas import (
    VoicePersonalityRecord,
    VoicePersonalityRecordResponse,
    UserVoicePersonalitiesResponse,
)
from app.voice_personalities.voice_personality_engine import normalize_personality
from app.services.engine_registry import voice_personality_engine

# Router exposed to FastAPI as voice_personalities_router in main.py.
voice_personalities_router = APIRouter(tags=["voice_personalities"])


def parse_path_personality(personality: str) -> str:
    """Decode URL path personality names so spaces work in GET, PUT, and DELETE."""
    return unquote(personality.replace("+", " "))


@voice_personalities_router.post(
    "/voice_personalities/{user_id}",
    response_model=VoicePersonalityRecordResponse,
    summary="Create voice personality record",
    description="Create a new voice personality record for the specified user.",
)
async def create_voice_personality_record(
    user_id: str,
    request: VoicePersonalityRecord,
) -> VoicePersonalityRecordResponse:
    """Create and return a voice personality record."""
    if voice_personality_engine.personality_exists(user_id, request.personality):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Personality already exists",
        )

    record = voice_personality_engine.create_record(user_id, request)
    return VoicePersonalityRecordResponse.from_record(record)


@voice_personalities_router.get(
    "/voice_personalities/{user_id}",
    response_model=UserVoicePersonalitiesResponse,
    summary="Get all voice personality records",
    description="Return all voice personality records saved by the specified user.",
)
async def get_voice_personality_records(
    user_id: str,
) -> UserVoicePersonalitiesResponse:
    """Return all voice personality records for a user."""
    records = voice_personality_engine.get_records(user_id)
    return UserVoicePersonalitiesResponse(
        user_id=user_id,
        voice_personalities=[
            VoicePersonalityRecordResponse.from_record(record)
            for record in records
        ],
    )


@voice_personalities_router.get(
    "/voice_personalities/{user_id}/{personality}",
    response_model=VoicePersonalityRecordResponse,
    summary="Get one voice personality record",
    description="Return one voice personality record identified by personality name.",
)
async def get_voice_personality_record(
    user_id: str,
    personality: str,
) -> VoicePersonalityRecordResponse:
    """Return a single voice personality record by name."""
    decoded_personality = parse_path_personality(personality)
    record = voice_personality_engine.get_record(user_id, decoded_personality)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Personality not found",
        )

    return VoicePersonalityRecordResponse.from_record(record)


@voice_personalities_router.put(
    "/voice_personalities/{user_id}/{personality}",
    response_model=VoicePersonalityRecordResponse,
    status_code=status.HTTP_200_OK,
    summary="Update voice personality record",
    description="Replace an existing voice personality record with updated data.",
)
async def update_voice_personality_record(
    user_id: str,
    personality: str,
    request: VoicePersonalityRecord,
) -> VoicePersonalityRecordResponse:
    """Update and return a voice personality record."""
    decoded_personality = parse_path_personality(personality)

    # Allow keeping the same personality while changing tone/energy.
    if normalize_personality(request.personality) != normalize_personality(
        decoded_personality
    ):
        if voice_personality_engine.personality_exists(user_id, request.personality):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Personality already exists",
            )

    record = voice_personality_engine.update_record(
        user_id,
        decoded_personality,
        request,
    )
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Personality not found",
        )

    return VoicePersonalityRecordResponse.from_record(record)


@voice_personalities_router.delete(
    "/voice_personalities/{user_id}/{personality}",
    response_model=VoicePersonalityRecordResponse,
    summary="Delete voice personality record",
    description="Delete a voice personality record and return the removed record.",
)
async def delete_voice_personality_record(
    user_id: str,
    personality: str,
) -> VoicePersonalityRecordResponse:
    """Delete a voice personality record and return the deleted item."""
    decoded_personality = parse_path_personality(personality)
    record = voice_personality_engine.delete_record(user_id, decoded_personality)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Personality not found",
        )

    return VoicePersonalityRecordResponse.from_record(record)
