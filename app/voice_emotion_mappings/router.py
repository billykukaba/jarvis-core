"""FastAPI routes for the Voice Emotion Mapping Engine (Module 66)."""

from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, status

from app.voice_emotion_mappings.schemas import (
    VoiceEmotionMappingRecord,
    VoiceEmotionMappingRecordResponse,
    UserVoiceEmotionMappingsResponse,
)
from app.voice_emotion_mappings.voice_emotion_mapping_engine import normalize_emotion
from app.services.engine_registry import voice_emotion_mapping_engine

# Router exposed to FastAPI as voice_emotion_mappings_router in main.py.
voice_emotion_mappings_router = APIRouter(tags=["voice_emotion_mappings"])


def parse_path_emotion(emotion: str) -> str:
    """Decode URL path emotion names so spaces work in GET, PUT, and DELETE."""
    return unquote(emotion.replace("+", " "))


@voice_emotion_mappings_router.post(
    "/voice_emotion_mappings/{user_id}",
    response_model=VoiceEmotionMappingRecordResponse,
    summary="Create voice emotion mapping record",
    description="Create a new voice emotion mapping record for the specified user.",
)
async def create_voice_emotion_mapping_record(
    user_id: str,
    request: VoiceEmotionMappingRecord,
) -> VoiceEmotionMappingRecordResponse:
    """Create and return a voice emotion mapping record."""
    if voice_emotion_mapping_engine.emotion_exists(user_id, request.emotion):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Emotion already exists",
        )

    record = voice_emotion_mapping_engine.create_record(user_id, request)
    return VoiceEmotionMappingRecordResponse.from_record(record)


@voice_emotion_mappings_router.get(
    "/voice_emotion_mappings/{user_id}",
    response_model=UserVoiceEmotionMappingsResponse,
    summary="Get all voice emotion mapping records",
    description="Return all voice emotion mapping records saved by the specified user.",
)
async def get_voice_emotion_mapping_records(
    user_id: str,
) -> UserVoiceEmotionMappingsResponse:
    """Return all voice emotion mapping records for a user."""
    records = voice_emotion_mapping_engine.get_records(user_id)
    return UserVoiceEmotionMappingsResponse(
        user_id=user_id,
        voice_emotion_mappings=[
            VoiceEmotionMappingRecordResponse.from_record(record)
            for record in records
        ],
    )


@voice_emotion_mappings_router.get(
    "/voice_emotion_mappings/{user_id}/{emotion}",
    response_model=VoiceEmotionMappingRecordResponse,
    summary="Get one voice emotion mapping record",
    description="Return one voice emotion mapping record identified by emotion name.",
)
async def get_voice_emotion_mapping_record(
    user_id: str,
    emotion: str,
) -> VoiceEmotionMappingRecordResponse:
    """Return a single voice emotion mapping record by name."""
    decoded_emotion = parse_path_emotion(emotion)
    record = voice_emotion_mapping_engine.get_record(user_id, decoded_emotion)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Emotion not found",
        )

    return VoiceEmotionMappingRecordResponse.from_record(record)


@voice_emotion_mappings_router.put(
    "/voice_emotion_mappings/{user_id}/{emotion}",
    response_model=VoiceEmotionMappingRecordResponse,
    status_code=status.HTTP_200_OK,
    summary="Update voice emotion mapping record",
    description="Replace an existing voice emotion mapping record with updated data.",
)
async def update_voice_emotion_mapping_record(
    user_id: str,
    emotion: str,
    request: VoiceEmotionMappingRecord,
) -> VoiceEmotionMappingRecordResponse:
    """Update and return a voice emotion mapping record."""
    decoded_emotion = parse_path_emotion(emotion)

    # Allow keeping the same emotion while changing voice_style/speech_speed.
    if normalize_emotion(request.emotion) != normalize_emotion(decoded_emotion):
        if voice_emotion_mapping_engine.emotion_exists(user_id, request.emotion):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Emotion already exists",
            )

    record = voice_emotion_mapping_engine.update_record(
        user_id,
        decoded_emotion,
        request,
    )
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Emotion not found",
        )

    return VoiceEmotionMappingRecordResponse.from_record(record)


@voice_emotion_mappings_router.delete(
    "/voice_emotion_mappings/{user_id}/{emotion}",
    response_model=VoiceEmotionMappingRecordResponse,
    summary="Delete voice emotion mapping record",
    description="Delete a voice emotion mapping record and return the removed record.",
)
async def delete_voice_emotion_mapping_record(
    user_id: str,
    emotion: str,
) -> VoiceEmotionMappingRecordResponse:
    """Delete a voice emotion mapping record and return the deleted item."""
    decoded_emotion = parse_path_emotion(emotion)
    record = voice_emotion_mapping_engine.delete_record(user_id, decoded_emotion)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Emotion not found",
        )

    return VoiceEmotionMappingRecordResponse.from_record(record)
