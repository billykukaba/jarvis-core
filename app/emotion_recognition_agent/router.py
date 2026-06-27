"""FastAPI routes for the Emotion Recognition Agent."""

from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, status

from app.emotion_recognition_agent.emotion_recognition_agent_engine import (
    normalize_emotion_id,
)
from app.emotion_recognition_agent.schemas import (
    EmotionRecognition,
    EmotionRecognitionResponse,
    UserEmotionRecognitionAgentResponse,
)
from app.services.engine_registry import emotion_recognition_agent_engine

# Router exposed to FastAPI as emotion_recognition_agent_router in main.py.
emotion_recognition_agent_router = APIRouter(tags=["Emotion Recognition Agent"])


def parse_path_emotion_id(emotion_id: str) -> str:
    """Decode URL path emotion IDs so spaces work in GET, PUT, and DELETE."""
    return unquote(emotion_id.replace("+", " "))


@emotion_recognition_agent_router.post(
    "/emotion_recognition_agent/{user_id}",
    response_model=EmotionRecognitionResponse,
    summary="Create emotion record",
    description="Create a new emotion recognition record for the specified user.",
)
async def create_emotion_record(
    user_id: str,
    request: EmotionRecognition,
) -> EmotionRecognitionResponse:
    """Create and return an emotion recognition record."""
    if emotion_recognition_agent_engine.emotion_id_exists(user_id, request.emotion_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Emotion record already exists",
        )

    record = emotion_recognition_agent_engine.create_record(user_id, request)
    return EmotionRecognitionResponse.from_emotion(record)


@emotion_recognition_agent_router.get(
    "/emotion_recognition_agent/{user_id}",
    response_model=UserEmotionRecognitionAgentResponse,
    summary="Get all emotion records",
    description="Return all emotion recognition records saved by the specified user.",
)
async def get_emotion_records(
    user_id: str,
) -> UserEmotionRecognitionAgentResponse:
    """Return all emotion recognition records for a user."""
    records = emotion_recognition_agent_engine.get_records(user_id)
    return UserEmotionRecognitionAgentResponse(
        user_id=user_id,
        emotion_records=[
            EmotionRecognitionResponse.from_emotion(record) for record in records
        ],
    )


@emotion_recognition_agent_router.get(
    "/emotion_recognition_agent/{user_id}/{emotion_id}",
    response_model=EmotionRecognitionResponse,
    summary="Get one emotion record",
    description="Return one emotion recognition record identified by emotion ID.",
)
async def get_emotion_record(
    user_id: str,
    emotion_id: str,
) -> EmotionRecognitionResponse:
    """Return a single emotion recognition record by ID."""
    decoded_id = parse_path_emotion_id(emotion_id)
    record = emotion_recognition_agent_engine.get_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Emotion record not found",
        )

    return EmotionRecognitionResponse.from_emotion(record)


@emotion_recognition_agent_router.put(
    "/emotion_recognition_agent/{user_id}/{emotion_id}",
    response_model=EmotionRecognitionResponse,
    status_code=status.HTTP_200_OK,
    summary="Update emotion record",
    description="Replace an existing emotion recognition record with updated data.",
)
async def update_emotion_record(
    user_id: str,
    emotion_id: str,
    request: EmotionRecognition,
) -> EmotionRecognitionResponse:
    """Update and return an emotion recognition record."""
    decoded_id = parse_path_emotion_id(emotion_id)

    if normalize_emotion_id(request.emotion_id) != normalize_emotion_id(decoded_id):
        if emotion_recognition_agent_engine.emotion_id_exists(
            user_id,
            request.emotion_id,
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Emotion record already exists",
            )

    record = emotion_recognition_agent_engine.update_record(
        user_id,
        decoded_id,
        request,
    )
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Emotion record not found",
        )

    return EmotionRecognitionResponse.from_emotion(record)


@emotion_recognition_agent_router.delete(
    "/emotion_recognition_agent/{user_id}/{emotion_id}",
    response_model=EmotionRecognitionResponse,
    summary="Delete emotion record",
    description="Delete an emotion recognition record and return the removed record.",
)
async def delete_emotion_record(
    user_id: str,
    emotion_id: str,
) -> EmotionRecognitionResponse:
    """Delete an emotion recognition record and return the deleted item."""
    decoded_id = parse_path_emotion_id(emotion_id)
    record = emotion_recognition_agent_engine.delete_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Emotion record not found",
        )

    return EmotionRecognitionResponse.from_emotion(record)
