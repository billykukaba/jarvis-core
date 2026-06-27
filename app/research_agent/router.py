"""FastAPI routes for the Research Agent."""

from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, status

from app.research_agent.research_agent_engine import normalize_research_id
from app.research_agent.schemas import (
    ResearchRecord,
    ResearchRecordResponse,
    UserResearchAgentResponse,
)
from app.services.engine_registry import research_agent_engine

# Router exposed to FastAPI as research_agent_router in main.py.
research_agent_router = APIRouter(tags=["Research Agent"])


def parse_path_research_id(research_id: str) -> str:
    """Decode URL path research IDs so spaces work in GET, PUT, and DELETE."""
    return unquote(research_id.replace("+", " "))


@research_agent_router.post(
    "/research_agent/{user_id}",
    response_model=ResearchRecordResponse,
    summary="Create research record",
    description="Create a new research record for the specified user.",
)
async def create_research_record(
    user_id: str,
    request: ResearchRecord,
) -> ResearchRecordResponse:
    """Create and return a research record."""
    if research_agent_engine.research_id_exists(user_id, request.research_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Research already exists",
        )

    record = research_agent_engine.create_record(user_id, request)
    return ResearchRecordResponse.from_record(record)


@research_agent_router.get(
    "/research_agent/{user_id}",
    response_model=UserResearchAgentResponse,
    summary="Get all research records",
    description="Return all research records saved by the specified user.",
)
async def get_research_records(user_id: str) -> UserResearchAgentResponse:
    """Return all research records for a user."""
    records = research_agent_engine.get_records(user_id)
    return UserResearchAgentResponse(
        user_id=user_id,
        research_records=[
            ResearchRecordResponse.from_record(record) for record in records
        ],
    )


@research_agent_router.get(
    "/research_agent/{user_id}/{research_id}",
    response_model=ResearchRecordResponse,
    summary="Get one research record",
    description="Return one research record identified by research ID.",
)
async def get_research_record(
    user_id: str,
    research_id: str,
) -> ResearchRecordResponse:
    """Return a single research record by ID."""
    decoded_id = parse_path_research_id(research_id)
    record = research_agent_engine.get_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Research not found",
        )

    return ResearchRecordResponse.from_record(record)


@research_agent_router.put(
    "/research_agent/{user_id}/{research_id}",
    response_model=ResearchRecordResponse,
    status_code=status.HTTP_200_OK,
    summary="Update research record",
    description="Replace an existing research record with updated data.",
)
async def update_research_record(
    user_id: str,
    research_id: str,
    request: ResearchRecord,
) -> ResearchRecordResponse:
    """Update and return a research record."""
    decoded_id = parse_path_research_id(research_id)

    if normalize_research_id(request.research_id) != normalize_research_id(decoded_id):
        if research_agent_engine.research_id_exists(user_id, request.research_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Research already exists",
            )

    record = research_agent_engine.update_record(user_id, decoded_id, request)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Research not found",
        )

    return ResearchRecordResponse.from_record(record)


@research_agent_router.delete(
    "/research_agent/{user_id}/{research_id}",
    response_model=ResearchRecordResponse,
    summary="Delete research record",
    description="Delete a research record and return the removed record.",
)
async def delete_research_record(
    user_id: str,
    research_id: str,
) -> ResearchRecordResponse:
    """Delete a research record and return the deleted item."""
    decoded_id = parse_path_research_id(research_id)
    record = research_agent_engine.delete_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Research not found",
        )

    return ResearchRecordResponse.from_record(record)
