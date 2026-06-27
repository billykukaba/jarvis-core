"""FastAPI routes for the Autonomous Research Engine.

Coordinates Browser Agent, News Monitoring Agent and Website Automation Agent
to perform autonomous research missions for Jarvis.
"""

from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, status

from app.autonomous_research_engine.autonomous_research_engine_engine import (
    normalize_research_id,
)
from app.autonomous_research_engine.schemas import (
    AutonomousResearchRecord,
    AutonomousResearchRecordResponse,
    UserAutonomousResearchEngineResponse,
)
from app.services.engine_registry import autonomous_research_engine

# Router exposed to FastAPI as autonomous_research_engine_router in main.py.
autonomous_research_engine_router = APIRouter(tags=["Autonomous Research Engine"])


def parse_path_research_id(research_id: str) -> str:
    """Decode URL path research IDs so spaces work in GET, PUT, and DELETE."""
    return unquote(research_id.replace("+", " "))


@autonomous_research_engine_router.post(
    "/autonomous_research_engine/{user_id}",
    response_model=AutonomousResearchRecordResponse,
    summary="Create research record",
    description=(
        "Create a new autonomous research record for the specified user. "
        "Coordinates Browser Agent, News Monitoring Agent and Website Automation "
        "Agent to perform autonomous research missions for Jarvis."
    ),
)
async def create_autonomous_research_record(
    user_id: str,
    request: AutonomousResearchRecord,
) -> AutonomousResearchRecordResponse:
    """Create and return an autonomous research record."""
    if autonomous_research_engine.research_id_exists(user_id, request.research_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Research record already exists",
        )

    record = autonomous_research_engine.create_record(user_id, request)
    return AutonomousResearchRecordResponse.from_record(record)


@autonomous_research_engine_router.get(
    "/autonomous_research_engine/{user_id}",
    response_model=UserAutonomousResearchEngineResponse,
    summary="Get all research records",
    description=(
        "Return all autonomous research records saved by the specified user. "
        "Coordinates Browser Agent, News Monitoring Agent and Website Automation "
        "Agent to perform autonomous research missions for Jarvis."
    ),
)
async def get_autonomous_research_records(
    user_id: str,
) -> UserAutonomousResearchEngineResponse:
    """Return all autonomous research records for a user."""
    records = autonomous_research_engine.get_records(user_id)
    return UserAutonomousResearchEngineResponse(
        user_id=user_id,
        research_records=[
            AutonomousResearchRecordResponse.from_record(record)
            for record in records
        ],
    )


@autonomous_research_engine_router.get(
    "/autonomous_research_engine/{user_id}/{research_id}",
    response_model=AutonomousResearchRecordResponse,
    summary="Get one research record",
    description="Return one autonomous research record identified by research ID.",
)
async def get_autonomous_research_record(
    user_id: str,
    research_id: str,
) -> AutonomousResearchRecordResponse:
    """Return a single autonomous research record by ID."""
    decoded_id = parse_path_research_id(research_id)
    record = autonomous_research_engine.get_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Research record not found",
        )

    return AutonomousResearchRecordResponse.from_record(record)


@autonomous_research_engine_router.put(
    "/autonomous_research_engine/{user_id}/{research_id}",
    response_model=AutonomousResearchRecordResponse,
    status_code=status.HTTP_200_OK,
    summary="Update research record",
    description="Replace an existing autonomous research record with updated data.",
)
async def update_autonomous_research_record(
    user_id: str,
    research_id: str,
    request: AutonomousResearchRecord,
) -> AutonomousResearchRecordResponse:
    """Update and return an autonomous research record."""
    decoded_id = parse_path_research_id(research_id)

    if normalize_research_id(request.research_id) != normalize_research_id(
        decoded_id,
    ):
        if autonomous_research_engine.research_id_exists(user_id, request.research_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Research record already exists",
            )

    record = autonomous_research_engine.update_record(
        user_id,
        decoded_id,
        request,
    )
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Research record not found",
        )

    return AutonomousResearchRecordResponse.from_record(record)


@autonomous_research_engine_router.delete(
    "/autonomous_research_engine/{user_id}/{research_id}",
    response_model=AutonomousResearchRecordResponse,
    summary="Delete research record",
    description="Delete an autonomous research record and return the removed record.",
)
async def delete_autonomous_research_record(
    user_id: str,
    research_id: str,
) -> AutonomousResearchRecordResponse:
    """Delete an autonomous research record and return the deleted item."""
    decoded_id = parse_path_research_id(research_id)
    record = autonomous_research_engine.delete_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Research record not found",
        )

    return AutonomousResearchRecordResponse.from_record(record)
