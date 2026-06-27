"""FastAPI routes for the Relationship Engine.

Manages relationships between users, goals, projects, memories, agents and knowledge
entities inside Jarvis.
"""

from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, status

from app.relationship_engine.relationship_engine_engine import normalize_relationship_id
from app.relationship_engine.schemas import (
    RelationshipRecord,
    RelationshipRecordResponse,
    UserRelationshipEngineResponse,
)
from app.services.engine_registry import relationship_engine

# Router exposed to FastAPI as relationship_engine_router in main.py.
relationship_engine_router = APIRouter(tags=["Relationship Engine"])


def parse_path_relationship_id(relationship_id: str) -> str:
    """Decode URL path relationship IDs so spaces work in GET, PUT, and DELETE."""
    return unquote(relationship_id.replace("+", " "))


@relationship_engine_router.post(
    "/relationship_engine/{user_id}",
    response_model=RelationshipRecordResponse,
    summary="Create relationship record",
    description=(
        "Create a new relationship record for the specified user. "
        "Manages relationships between users, goals, projects, memories, agents "
        "and knowledge entities inside Jarvis."
    ),
)
async def create_relationship_record(
    user_id: str,
    request: RelationshipRecord,
) -> RelationshipRecordResponse:
    """Create and return a relationship record."""
    if relationship_engine.relationship_id_exists(user_id, request.relationship_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Relationship record already exists",
        )

    record = relationship_engine.create_record(user_id, request)
    return RelationshipRecordResponse.from_record(record)


@relationship_engine_router.get(
    "/relationship_engine/{user_id}",
    response_model=UserRelationshipEngineResponse,
    summary="Get all relationship records",
    description=(
        "Return all relationship records saved by the specified user. "
        "Manages relationships between users, goals, projects, memories, agents "
        "and knowledge entities inside Jarvis."
    ),
)
async def get_relationship_records(
    user_id: str,
) -> UserRelationshipEngineResponse:
    """Return all relationship records for a user."""
    records = relationship_engine.get_records(user_id)
    return UserRelationshipEngineResponse(
        user_id=user_id,
        relationship_records=[
            RelationshipRecordResponse.from_record(record) for record in records
        ],
    )


@relationship_engine_router.get(
    "/relationship_engine/{user_id}/{relationship_id}",
    response_model=RelationshipRecordResponse,
    summary="Get one relationship record",
    description="Return one relationship record identified by relationship ID.",
)
async def get_relationship_record(
    user_id: str,
    relationship_id: str,
) -> RelationshipRecordResponse:
    """Return a single relationship record by ID."""
    decoded_id = parse_path_relationship_id(relationship_id)
    record = relationship_engine.get_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relationship record not found",
        )

    return RelationshipRecordResponse.from_record(record)


@relationship_engine_router.put(
    "/relationship_engine/{user_id}/{relationship_id}",
    response_model=RelationshipRecordResponse,
    status_code=status.HTTP_200_OK,
    summary="Update relationship record",
    description="Replace an existing relationship record with updated data.",
)
async def update_relationship_record(
    user_id: str,
    relationship_id: str,
    request: RelationshipRecord,
) -> RelationshipRecordResponse:
    """Update and return a relationship record."""
    decoded_id = parse_path_relationship_id(relationship_id)

    if normalize_relationship_id(
        request.relationship_id,
    ) != normalize_relationship_id(decoded_id):
        if relationship_engine.relationship_id_exists(user_id, request.relationship_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Relationship record already exists",
            )

    record = relationship_engine.update_record(
        user_id,
        decoded_id,
        request,
    )
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relationship record not found",
        )

    return RelationshipRecordResponse.from_record(record)


@relationship_engine_router.delete(
    "/relationship_engine/{user_id}/{relationship_id}",
    response_model=RelationshipRecordResponse,
    summary="Delete relationship record",
    description="Delete a relationship record and return the removed record.",
)
async def delete_relationship_record(
    user_id: str,
    relationship_id: str,
) -> RelationshipRecordResponse:
    """Delete a relationship record and return the deleted item."""
    decoded_id = parse_path_relationship_id(relationship_id)
    record = relationship_engine.delete_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relationship record not found",
        )

    return RelationshipRecordResponse.from_record(record)
