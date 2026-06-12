"""FastAPI routes for the Emotion Service (Module 62)."""

from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, status

from app.emotions.emotion_service_engine import normalize_emotion
from app.emotions.schemas import (
    EmotionRecord,
    EmotionRecordResponse,
    UserEmotionsResponse,
)
from app.services.engine_registry import emotion_service_engine

# Router exposed to FastAPI as emotions_router in main.py.
emotions_router = APIRouter(tags=["emotions"])


def parse_path_emotion(emotion: str) -> str:
    """Decode URL path emotion names so spaces work in GET, PUT, and DELETE."""
    return unquote(emotion.replace("+", " "))


@emotions_router.post(
    "/emotions/{user_id}",
    response_model=EmotionRecordResponse,
    summary="Create emotion record",
    description="Create a new emotion record for the specified user.",
)
async def create_emotion_record(
    user_id: str,
    request: EmotionRecord,
) -> EmotionRecordResponse:
    """Create and return an emotion record."""
    if emotion_service_engine.emotion_exists(user_id, request.emotion):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Emotion already exists",
        )

    record = emotion_service_engine.create_record(user_id, request)
    return EmotionRecordResponse.from_record(record)


@emotions_router.get(
    "/emotions/{user_id}",
    response_model=UserEmotionsResponse,
    summary="Get all emotion records",
    description="Return all emotion records saved by the specified user.",
)
async def get_emotion_records(user_id: str) -> UserEmotionsResponse:
    """Return all emotion records for a user."""
    records = emotion_service_engine.get_records(user_id)
    return UserEmotionsResponse(
        user_id=user_id,
        emotions=[
            EmotionRecordResponse.from_record(record) for record in records
        ],
    )


@emotions_router.get(
    "/emotions/{user_id}/{emotion}",
    response_model=EmotionRecordResponse,
    summary="Get one emotion record",
    description="Return one emotion record identified by emotion name.",
)
async def get_emotion_record(
    user_id: str,
    emotion: str,
) -> EmotionRecordResponse:
    """Return a single emotion record by name."""
    decoded_emotion = parse_path_emotion(emotion)
    record = emotion_service_engine.get_record(user_id, decoded_emotion)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Emotion not found",
        )

    return EmotionRecordResponse.from_record(record)


@emotions_router.put(
    "/emotions/{user_id}/{emotion}",
    response_model=EmotionRecordResponse,
    status_code=status.HTTP_200_OK,
    summary="Update emotion record",
    description="Replace an existing emotion record with updated data.",
)
async def update_emotion_record(
    user_id: str,
    emotion: str,
    request: EmotionRecord,
) -> EmotionRecordResponse:
    """Update and return an emotion record."""
    decoded_emotion = parse_path_emotion(emotion)

    # Allow keeping the same emotion while changing intensity.
    if normalize_emotion(request.emotion) != normalize_emotion(decoded_emotion):
        if emotion_service_engine.emotion_exists(user_id, request.emotion):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Emotion already exists",
            )

    record = emotion_service_engine.update_record(
        user_id,
        decoded_emotion,
        request,
    )
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Emotion not found",
        )

    return EmotionRecordResponse.from_record(record)


@emotions_router.delete(
    "/emotions/{user_id}/{emotion}",
    response_model=EmotionRecordResponse,
    summary="Delete emotion record",
    description="Delete an emotion record and return the removed record.",
)
async def delete_emotion_record(
    user_id: str,
    emotion: str,
) -> EmotionRecordResponse:
    """Delete an emotion record and return the deleted item."""
    decoded_emotion = parse_path_emotion(emotion)
    record = emotion_service_engine.delete_record(user_id, decoded_emotion)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Emotion not found",
        )

    return EmotionRecordResponse.from_record(record)
