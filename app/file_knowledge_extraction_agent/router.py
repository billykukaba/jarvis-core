"""FastAPI routes for the File Knowledge Extraction Agent.

Extracts structured knowledge, concepts, entities and summaries from documents
for Jarvis Knowledge System.
"""

from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, status

from app.file_knowledge_extraction_agent.file_knowledge_extraction_agent_engine import (
    normalize_knowledge_id,
)
from app.file_knowledge_extraction_agent.schemas import (
    FileKnowledgeExtractionRecord,
    FileKnowledgeExtractionRecordResponse,
    UserFileKnowledgeExtractionAgentResponse,
)
from app.services.engine_registry import file_knowledge_extraction_agent_engine

# Router exposed to FastAPI as file_knowledge_extraction_agent_router in main.py.
file_knowledge_extraction_agent_router = APIRouter(
    tags=["File Knowledge Extraction Agent"],
)


def parse_path_knowledge_id(knowledge_id: str) -> str:
    """Decode URL path knowledge IDs so spaces work in GET, PUT, and DELETE."""
    return unquote(knowledge_id.replace("+", " "))


@file_knowledge_extraction_agent_router.post(
    "/file_knowledge_extraction_agent/{user_id}",
    response_model=FileKnowledgeExtractionRecordResponse,
    summary="Create knowledge extraction record",
    description=(
        "Create a new knowledge extraction record for the specified user. "
        "Extracts structured knowledge, concepts, entities and summaries from "
        "documents for Jarvis Knowledge System."
    ),
)
async def create_file_knowledge_extraction_record(
    user_id: str,
    request: FileKnowledgeExtractionRecord,
) -> FileKnowledgeExtractionRecordResponse:
    """Create and return a knowledge extraction record."""
    if file_knowledge_extraction_agent_engine.knowledge_id_exists(
        user_id,
        request.knowledge_id,
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Knowledge extraction record already exists",
        )

    record = file_knowledge_extraction_agent_engine.create_record(user_id, request)
    return FileKnowledgeExtractionRecordResponse.from_record(record)


@file_knowledge_extraction_agent_router.get(
    "/file_knowledge_extraction_agent/{user_id}",
    response_model=UserFileKnowledgeExtractionAgentResponse,
    summary="Get all knowledge extraction records",
    description=(
        "Return all knowledge extraction records saved by the specified user. "
        "Extracts structured knowledge, concepts, entities and summaries from "
        "documents for Jarvis Knowledge System."
    ),
)
async def get_file_knowledge_extraction_records(
    user_id: str,
) -> UserFileKnowledgeExtractionAgentResponse:
    """Return all knowledge extraction records for a user."""
    records = file_knowledge_extraction_agent_engine.get_records(user_id)
    return UserFileKnowledgeExtractionAgentResponse(
        user_id=user_id,
        knowledge_records=[
            FileKnowledgeExtractionRecordResponse.from_record(record)
            for record in records
        ],
    )


@file_knowledge_extraction_agent_router.get(
    "/file_knowledge_extraction_agent/{user_id}/{knowledge_id}",
    response_model=FileKnowledgeExtractionRecordResponse,
    summary="Get one knowledge extraction record",
    description="Return one knowledge extraction record identified by knowledge ID.",
)
async def get_file_knowledge_extraction_record(
    user_id: str,
    knowledge_id: str,
) -> FileKnowledgeExtractionRecordResponse:
    """Return a single knowledge extraction record by ID."""
    decoded_id = parse_path_knowledge_id(knowledge_id)
    record = file_knowledge_extraction_agent_engine.get_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Knowledge extraction record not found",
        )

    return FileKnowledgeExtractionRecordResponse.from_record(record)


@file_knowledge_extraction_agent_router.put(
    "/file_knowledge_extraction_agent/{user_id}/{knowledge_id}",
    response_model=FileKnowledgeExtractionRecordResponse,
    status_code=status.HTTP_200_OK,
    summary="Update knowledge extraction record",
    description="Replace an existing knowledge extraction record with updated data.",
)
async def update_file_knowledge_extraction_record(
    user_id: str,
    knowledge_id: str,
    request: FileKnowledgeExtractionRecord,
) -> FileKnowledgeExtractionRecordResponse:
    """Update and return a knowledge extraction record."""
    decoded_id = parse_path_knowledge_id(knowledge_id)

    if normalize_knowledge_id(request.knowledge_id) != normalize_knowledge_id(
        decoded_id,
    ):
        if file_knowledge_extraction_agent_engine.knowledge_id_exists(
            user_id,
            request.knowledge_id,
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Knowledge extraction record already exists",
            )

    record = file_knowledge_extraction_agent_engine.update_record(
        user_id,
        decoded_id,
        request,
    )
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Knowledge extraction record not found",
        )

    return FileKnowledgeExtractionRecordResponse.from_record(record)


@file_knowledge_extraction_agent_router.delete(
    "/file_knowledge_extraction_agent/{user_id}/{knowledge_id}",
    response_model=FileKnowledgeExtractionRecordResponse,
    summary="Delete knowledge extraction record",
    description="Delete a knowledge extraction record and return the removed record.",
)
async def delete_file_knowledge_extraction_record(
    user_id: str,
    knowledge_id: str,
) -> FileKnowledgeExtractionRecordResponse:
    """Delete a knowledge extraction record and return the deleted item."""
    decoded_id = parse_path_knowledge_id(knowledge_id)
    record = file_knowledge_extraction_agent_engine.delete_record(
        user_id,
        decoded_id,
    )
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Knowledge extraction record not found",
        )

    return FileKnowledgeExtractionRecordResponse.from_record(record)
