"""FastAPI routes for the Research Service (Module 53)."""

from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, status

from app.research.research_service_engine import normalize_title
from app.research.schemas import (
    ResearchRecord,
    ResearchRecordResponse,
    UserResearchResponse,
)
from app.services.engine_registry import research_service_engine

# Router exposed to FastAPI as research_router in main.py.
research_router = APIRouter(tags=["research"])


def parse_path_title(title: str) -> str:
    """Decode URL path titles so spaces work in GET, PUT, and DELETE."""
    return unquote(title.replace("+", " "))


@research_router.post(
    "/research/{user_id}",
    response_model=ResearchRecordResponse,
    summary="Create research record",
    description="Create a new research record for the specified user.",
)
async def create_research_record(
    user_id: str,
    request: ResearchRecord,
) -> ResearchRecordResponse:
    """Create and return a research record."""
    if research_service_engine.title_exists(user_id, request.title):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Research record already exists",
        )

    record = research_service_engine.create_record(user_id, request)
    return ResearchRecordResponse.from_record(record)


@research_router.get(
    "/research/{user_id}",
    response_model=UserResearchResponse,
    summary="Get all research records",
    description="Return all research records saved by the specified user.",
)
async def get_research_records(user_id: str) -> UserResearchResponse:
    """Return all research records for a user."""
    records = research_service_engine.get_records(user_id)
    return UserResearchResponse(
        user_id=user_id,
        research=[
            ResearchRecordResponse.from_record(record) for record in records
        ],
    )


@research_router.get(
    "/research/{user_id}/{title}",
    response_model=ResearchRecordResponse,
    summary="Get one research record",
    description="Return one research record identified by title.",
)
async def get_research_record(user_id: str, title: str) -> ResearchRecordResponse:
    """Return a single research record by title."""
    decoded_title = parse_path_title(title)
    record = research_service_engine.get_record(user_id, decoded_title)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Research record not found",
        )

    return ResearchRecordResponse.from_record(record)


@research_router.put(
    "/research/{user_id}/{title}",
    response_model=ResearchRecordResponse,
    status_code=status.HTTP_200_OK,
    summary="Update research record",
    description="Replace an existing research record with updated data.",
)
async def update_research_record(
    user_id: str,
    title: str,
    request: ResearchRecord,
) -> ResearchRecordResponse:
    """Update and return a research record."""
    decoded_title = parse_path_title(title)

    # Allow keeping the same title while changing institution/year.
    if normalize_title(request.title) != normalize_title(decoded_title):
        if research_service_engine.title_exists(user_id, request.title):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Research record already exists",
            )

    record = research_service_engine.update_record(
        user_id,
        decoded_title,
        request,
    )
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Research record not found",
        )

    return ResearchRecordResponse.from_record(record)


@research_router.delete(
    "/research/{user_id}/{title}",
    response_model=ResearchRecordResponse,
    summary="Delete research record",
    description="Delete a research record and return the removed record.",
)
async def delete_research_record(
    user_id: str,
    title: str,
) -> ResearchRecordResponse:
    """Delete a research record and return the deleted item."""
    decoded_title = parse_path_title(title)
    record = research_service_engine.delete_record(user_id, decoded_title)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Research record not found",
        )

    return ResearchRecordResponse.from_record(record)
