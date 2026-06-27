"""FastAPI routes for the Speech To Text Agent."""

from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, status

from app.services.engine_registry import speech_to_text_agent_engine
from app.speech_to_text_agent.schemas import (
    SpeechRecord,
    SpeechRecordResponse,
    UserSpeechToTextAgentResponse,
)
from app.speech_to_text_agent.speech_to_text_agent_engine import normalize_speech_id

# Router exposed to FastAPI as speech_to_text_agent_router in main.py.
speech_to_text_agent_router = APIRouter(tags=["Speech To Text Agent"])


def parse_path_speech_id(speech_id: str) -> str:
    """Decode URL path speech IDs so spaces work in GET, PUT, and DELETE."""
    return unquote(speech_id.replace("+", " "))


@speech_to_text_agent_router.post(
    "/speech_to_text_agent/{user_id}",
    response_model=SpeechRecordResponse,
    summary="Create speech record",
    description="Create a new speech-to-text record for the specified user.",
)
async def create_speech_record(
    user_id: str,
    request: SpeechRecord,
) -> SpeechRecordResponse:
    """Create and return a speech record."""
    if speech_to_text_agent_engine.speech_id_exists(user_id, request.speech_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Speech record already exists",
        )

    record = speech_to_text_agent_engine.create_record(user_id, request)
    return SpeechRecordResponse.from_record(record)


@speech_to_text_agent_router.get(
    "/speech_to_text_agent/{user_id}",
    response_model=UserSpeechToTextAgentResponse,
    summary="Get all speech records",
    description="Return all speech-to-text records saved by the specified user.",
)
async def get_speech_records(user_id: str) -> UserSpeechToTextAgentResponse:
    """Return all speech records for a user."""
    records = speech_to_text_agent_engine.get_records(user_id)
    return UserSpeechToTextAgentResponse(
        user_id=user_id,
        speech_records=[
            SpeechRecordResponse.from_record(record) for record in records
        ],
    )


@speech_to_text_agent_router.get(
    "/speech_to_text_agent/{user_id}/{speech_id}",
    response_model=SpeechRecordResponse,
    summary="Get one speech record",
    description="Return one speech-to-text record identified by speech ID.",
)
async def get_speech_record(
    user_id: str,
    speech_id: str,
) -> SpeechRecordResponse:
    """Return a single speech record by ID."""
    decoded_id = parse_path_speech_id(speech_id)
    record = speech_to_text_agent_engine.get_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Speech record not found",
        )

    return SpeechRecordResponse.from_record(record)


@speech_to_text_agent_router.put(
    "/speech_to_text_agent/{user_id}/{speech_id}",
    response_model=SpeechRecordResponse,
    status_code=status.HTTP_200_OK,
    summary="Update speech record",
    description="Replace an existing speech-to-text record with updated data.",
)
async def update_speech_record(
    user_id: str,
    speech_id: str,
    request: SpeechRecord,
) -> SpeechRecordResponse:
    """Update and return a speech record."""
    decoded_id = parse_path_speech_id(speech_id)

    if normalize_speech_id(request.speech_id) != normalize_speech_id(decoded_id):
        if speech_to_text_agent_engine.speech_id_exists(user_id, request.speech_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Speech record already exists",
            )

    record = speech_to_text_agent_engine.update_record(user_id, decoded_id, request)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Speech record not found",
        )

    return SpeechRecordResponse.from_record(record)


@speech_to_text_agent_router.delete(
    "/speech_to_text_agent/{user_id}/{speech_id}",
    response_model=SpeechRecordResponse,
    summary="Delete speech record",
    description="Delete a speech-to-text record and return the removed record.",
)
async def delete_speech_record(
    user_id: str,
    speech_id: str,
) -> SpeechRecordResponse:
    """Delete a speech record and return the deleted item."""
    decoded_id = parse_path_speech_id(speech_id)
    record = speech_to_text_agent_engine.delete_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Speech record not found",
        )

    return SpeechRecordResponse.from_record(record)
