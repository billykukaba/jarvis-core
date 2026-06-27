"""FastAPI routes for the Text To Speech Agent."""

from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, status

from app.services.engine_registry import text_to_speech_agent_engine
from app.text_to_speech_agent.schemas import (
    TextToSpeechRecord,
    TextToSpeechRecordResponse,
    UserTextToSpeechAgentResponse,
)
from app.text_to_speech_agent.text_to_speech_agent_engine import normalize_tts_id

# Router exposed to FastAPI as text_to_speech_agent_router in main.py.
text_to_speech_agent_router = APIRouter(tags=["Text To Speech Agent"])


def parse_path_tts_id(tts_id: str) -> str:
    """Decode URL path TTS IDs so spaces work in GET, PUT, and DELETE."""
    return unquote(tts_id.replace("+", " "))


@text_to_speech_agent_router.post(
    "/text_to_speech_agent/{user_id}",
    response_model=TextToSpeechRecordResponse,
    summary="Create TTS record",
    description="Create a new text-to-speech record for the specified user.",
)
async def create_tts_record(
    user_id: str,
    request: TextToSpeechRecord,
) -> TextToSpeechRecordResponse:
    """Create and return a TTS record."""
    if text_to_speech_agent_engine.tts_id_exists(user_id, request.tts_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="TTS record already exists",
        )

    record = text_to_speech_agent_engine.create_record(user_id, request)
    return TextToSpeechRecordResponse.from_record(record)


@text_to_speech_agent_router.get(
    "/text_to_speech_agent/{user_id}",
    response_model=UserTextToSpeechAgentResponse,
    summary="Get all TTS records",
    description="Return all text-to-speech records saved by the specified user.",
)
async def get_tts_records(user_id: str) -> UserTextToSpeechAgentResponse:
    """Return all TTS records for a user."""
    records = text_to_speech_agent_engine.get_records(user_id)
    return UserTextToSpeechAgentResponse(
        user_id=user_id,
        tts_records=[
            TextToSpeechRecordResponse.from_record(record) for record in records
        ],
    )


@text_to_speech_agent_router.get(
    "/text_to_speech_agent/{user_id}/{tts_id}",
    response_model=TextToSpeechRecordResponse,
    summary="Get one TTS record",
    description="Return one text-to-speech record identified by TTS ID.",
)
async def get_tts_record(
    user_id: str,
    tts_id: str,
) -> TextToSpeechRecordResponse:
    """Return a single TTS record by ID."""
    decoded_id = parse_path_tts_id(tts_id)
    record = text_to_speech_agent_engine.get_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="TTS record not found",
        )

    return TextToSpeechRecordResponse.from_record(record)


@text_to_speech_agent_router.put(
    "/text_to_speech_agent/{user_id}/{tts_id}",
    response_model=TextToSpeechRecordResponse,
    status_code=status.HTTP_200_OK,
    summary="Update TTS record",
    description="Replace an existing text-to-speech record with updated data.",
)
async def update_tts_record(
    user_id: str,
    tts_id: str,
    request: TextToSpeechRecord,
) -> TextToSpeechRecordResponse:
    """Update and return a TTS record."""
    decoded_id = parse_path_tts_id(tts_id)

    if normalize_tts_id(request.tts_id) != normalize_tts_id(decoded_id):
        if text_to_speech_agent_engine.tts_id_exists(user_id, request.tts_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="TTS record already exists",
            )

    record = text_to_speech_agent_engine.update_record(user_id, decoded_id, request)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="TTS record not found",
        )

    return TextToSpeechRecordResponse.from_record(record)


@text_to_speech_agent_router.delete(
    "/text_to_speech_agent/{user_id}/{tts_id}",
    response_model=TextToSpeechRecordResponse,
    summary="Delete TTS record",
    description="Delete a text-to-speech record and return the removed record.",
)
async def delete_tts_record(
    user_id: str,
    tts_id: str,
) -> TextToSpeechRecordResponse:
    """Delete a TTS record and return the deleted item."""
    decoded_id = parse_path_tts_id(tts_id)
    record = text_to_speech_agent_engine.delete_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="TTS record not found",
        )

    return TextToSpeechRecordResponse.from_record(record)
