"""FastAPI routes for the Personal Knowledge Base Agent.

Stores, organizes and manages the user's long-term knowledge base for Jarvis Intelligence.
"""

from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, status

from app.personal_knowledge_base_agent.personal_knowledge_base_agent_engine import (
    normalize_knowledge_base_id,
)
from app.personal_knowledge_base_agent.schemas import (
    PersonalKnowledgeRecord,
    PersonalKnowledgeRecordResponse,
    UserPersonalKnowledgeBaseAgentResponse,
)
from app.services.engine_registry import personal_knowledge_base_agent_engine

# Router exposed to FastAPI as personal_knowledge_base_agent_router in main.py.
personal_knowledge_base_agent_router = APIRouter(
    tags=["Personal Knowledge Base Agent"],
)


def parse_path_knowledge_base_id(knowledge_base_id: str) -> str:
    """Decode URL path knowledge base IDs so spaces work in GET, PUT, and DELETE."""
    return unquote(knowledge_base_id.replace("+", " "))


@personal_knowledge_base_agent_router.post(
    "/personal_knowledge_base_agent/{user_id}",
    response_model=PersonalKnowledgeRecordResponse,
    summary="Create personal knowledge record",
    description=(
        "Create a new personal knowledge record for the specified user. "
        "Stores, organizes and manages the user's long-term knowledge base "
        "for Jarvis Intelligence."
    ),
)
async def create_personal_knowledge_record(
    user_id: str,
    request: PersonalKnowledgeRecord,
) -> PersonalKnowledgeRecordResponse:
    """Create and return a personal knowledge record."""
    if personal_knowledge_base_agent_engine.knowledge_base_id_exists(
        user_id,
        request.knowledge_base_id,
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Personal knowledge record already exists",
        )

    record = personal_knowledge_base_agent_engine.create_record(user_id, request)
    return PersonalKnowledgeRecordResponse.from_record(record)


@personal_knowledge_base_agent_router.get(
    "/personal_knowledge_base_agent/{user_id}",
    response_model=UserPersonalKnowledgeBaseAgentResponse,
    summary="Get all personal knowledge records",
    description=(
        "Return all personal knowledge records saved by the specified user. "
        "Stores, organizes and manages the user's long-term knowledge base "
        "for Jarvis Intelligence."
    ),
)
async def get_personal_knowledge_records(
    user_id: str,
) -> UserPersonalKnowledgeBaseAgentResponse:
    """Return all personal knowledge records for a user."""
    records = personal_knowledge_base_agent_engine.get_records(user_id)
    return UserPersonalKnowledgeBaseAgentResponse(
        user_id=user_id,
        knowledge_base_records=[
            PersonalKnowledgeRecordResponse.from_record(record)
            for record in records
        ],
    )


@personal_knowledge_base_agent_router.get(
    "/personal_knowledge_base_agent/{user_id}/{knowledge_base_id}",
    response_model=PersonalKnowledgeRecordResponse,
    summary="Get one personal knowledge record",
    description="Return one personal knowledge record identified by knowledge base ID.",
)
async def get_personal_knowledge_record(
    user_id: str,
    knowledge_base_id: str,
) -> PersonalKnowledgeRecordResponse:
    """Return a single personal knowledge record by ID."""
    decoded_id = parse_path_knowledge_base_id(knowledge_base_id)
    record = personal_knowledge_base_agent_engine.get_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Personal knowledge record not found",
        )

    return PersonalKnowledgeRecordResponse.from_record(record)


@personal_knowledge_base_agent_router.put(
    "/personal_knowledge_base_agent/{user_id}/{knowledge_base_id}",
    response_model=PersonalKnowledgeRecordResponse,
    status_code=status.HTTP_200_OK,
    summary="Update personal knowledge record",
    description="Replace an existing personal knowledge record with updated data.",
)
async def update_personal_knowledge_record(
    user_id: str,
    knowledge_base_id: str,
    request: PersonalKnowledgeRecord,
) -> PersonalKnowledgeRecordResponse:
    """Update and return a personal knowledge record."""
    decoded_id = parse_path_knowledge_base_id(knowledge_base_id)

    if normalize_knowledge_base_id(
        request.knowledge_base_id,
    ) != normalize_knowledge_base_id(decoded_id):
        if personal_knowledge_base_agent_engine.knowledge_base_id_exists(
            user_id,
            request.knowledge_base_id,
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Personal knowledge record already exists",
            )

    record = personal_knowledge_base_agent_engine.update_record(
        user_id,
        decoded_id,
        request,
    )
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Personal knowledge record not found",
        )

    return PersonalKnowledgeRecordResponse.from_record(record)


@personal_knowledge_base_agent_router.delete(
    "/personal_knowledge_base_agent/{user_id}/{knowledge_base_id}",
    response_model=PersonalKnowledgeRecordResponse,
    summary="Delete personal knowledge record",
    description="Delete a personal knowledge record and return the removed record.",
)
async def delete_personal_knowledge_record(
    user_id: str,
    knowledge_base_id: str,
) -> PersonalKnowledgeRecordResponse:
    """Delete a personal knowledge record and return the deleted item."""
    decoded_id = parse_path_knowledge_base_id(knowledge_base_id)
    record = personal_knowledge_base_agent_engine.delete_record(
        user_id,
        decoded_id,
    )
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Personal knowledge record not found",
        )

    return PersonalKnowledgeRecordResponse.from_record(record)
