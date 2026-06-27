"""FastAPI routes for the Face Recognition Agent."""

from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, status

from app.face_recognition_agent.face_recognition_agent_engine import normalize_face_id
from app.face_recognition_agent.schemas import (
    FaceRecognition,
    FaceRecognitionResponse,
    UserFaceRecognitionAgentResponse,
)
from app.services.engine_registry import face_recognition_agent_engine

# Router exposed to FastAPI as face_recognition_agent_router in main.py.
face_recognition_agent_router = APIRouter(tags=["Face Recognition Agent"])


def parse_path_face_id(face_id: str) -> str:
    """Decode URL path face IDs so spaces work in GET, PUT, and DELETE."""
    return unquote(face_id.replace("+", " "))


@face_recognition_agent_router.post(
    "/face_recognition_agent/{user_id}",
    response_model=FaceRecognitionResponse,
    summary="Create face record",
    description="Create a new face recognition record for the specified user.",
)
async def create_face_record(
    user_id: str,
    request: FaceRecognition,
) -> FaceRecognitionResponse:
    """Create and return a face recognition record."""
    if face_recognition_agent_engine.face_id_exists(user_id, request.face_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Face record already exists",
        )

    record = face_recognition_agent_engine.create_record(user_id, request)
    return FaceRecognitionResponse.from_face(record)


@face_recognition_agent_router.get(
    "/face_recognition_agent/{user_id}",
    response_model=UserFaceRecognitionAgentResponse,
    summary="Get all face records",
    description="Return all face recognition records saved by the specified user.",
)
async def get_face_records(user_id: str) -> UserFaceRecognitionAgentResponse:
    """Return all face recognition records for a user."""
    records = face_recognition_agent_engine.get_records(user_id)
    return UserFaceRecognitionAgentResponse(
        user_id=user_id,
        face_records=[
            FaceRecognitionResponse.from_face(record) for record in records
        ],
    )


@face_recognition_agent_router.get(
    "/face_recognition_agent/{user_id}/{face_id}",
    response_model=FaceRecognitionResponse,
    summary="Get one face record",
    description="Return one face recognition record identified by face ID.",
)
async def get_face_record(
    user_id: str,
    face_id: str,
) -> FaceRecognitionResponse:
    """Return a single face recognition record by ID."""
    decoded_id = parse_path_face_id(face_id)
    record = face_recognition_agent_engine.get_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Face record not found",
        )

    return FaceRecognitionResponse.from_face(record)


@face_recognition_agent_router.put(
    "/face_recognition_agent/{user_id}/{face_id}",
    response_model=FaceRecognitionResponse,
    status_code=status.HTTP_200_OK,
    summary="Update face record",
    description="Replace an existing face recognition record with updated data.",
)
async def update_face_record(
    user_id: str,
    face_id: str,
    request: FaceRecognition,
) -> FaceRecognitionResponse:
    """Update and return a face recognition record."""
    decoded_id = parse_path_face_id(face_id)

    if normalize_face_id(request.face_id) != normalize_face_id(decoded_id):
        if face_recognition_agent_engine.face_id_exists(user_id, request.face_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Face record already exists",
            )

    record = face_recognition_agent_engine.update_record(
        user_id,
        decoded_id,
        request,
    )
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Face record not found",
        )

    return FaceRecognitionResponse.from_face(record)


@face_recognition_agent_router.delete(
    "/face_recognition_agent/{user_id}/{face_id}",
    response_model=FaceRecognitionResponse,
    summary="Delete face record",
    description="Delete a face recognition record and return the removed record.",
)
async def delete_face_record(
    user_id: str,
    face_id: str,
) -> FaceRecognitionResponse:
    """Delete a face recognition record and return the deleted item."""
    decoded_id = parse_path_face_id(face_id)
    record = face_recognition_agent_engine.delete_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Face record not found",
        )

    return FaceRecognitionResponse.from_face(record)
