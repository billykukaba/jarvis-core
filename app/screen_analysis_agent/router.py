"""FastAPI routes for the Screen Analysis Agent."""

from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, status

from app.screen_analysis_agent.schemas import (
    ScreenAnalysisRecord,
    ScreenAnalysisRecordResponse,
    UserScreenAnalysisAgentResponse,
)
from app.screen_analysis_agent.screen_analysis_agent_engine import normalize_screen_id
from app.services.engine_registry import screen_analysis_agent_engine

# Router exposed to FastAPI as screen_analysis_agent_router in main.py.
screen_analysis_agent_router = APIRouter(tags=["Screen Analysis Agent"])


def parse_path_screen_id(screen_id: str) -> str:
    """Decode URL path screen IDs so spaces work in GET, PUT, and DELETE."""
    return unquote(screen_id.replace("+", " "))


@screen_analysis_agent_router.post(
    "/screen_analysis_agent/{user_id}",
    response_model=ScreenAnalysisRecordResponse,
    summary="Create screen analysis record",
    description="Create a new screen analysis record for the specified user.",
)
async def create_screen_analysis_record(
    user_id: str,
    request: ScreenAnalysisRecord,
) -> ScreenAnalysisRecordResponse:
    """Create and return a screen analysis record."""
    if screen_analysis_agent_engine.screen_id_exists(user_id, request.screen_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Screen analysis record already exists",
        )

    record = screen_analysis_agent_engine.create_record(user_id, request)
    return ScreenAnalysisRecordResponse.from_record(record)


@screen_analysis_agent_router.get(
    "/screen_analysis_agent/{user_id}",
    response_model=UserScreenAnalysisAgentResponse,
    summary="Get all screen analysis records",
    description="Return all screen analysis records saved by the specified user.",
)
async def get_screen_analysis_records(
    user_id: str,
) -> UserScreenAnalysisAgentResponse:
    """Return all screen analysis records for a user."""
    records = screen_analysis_agent_engine.get_records(user_id)
    return UserScreenAnalysisAgentResponse(
        user_id=user_id,
        screen_analysis_records=[
            ScreenAnalysisRecordResponse.from_record(record) for record in records
        ],
    )


@screen_analysis_agent_router.get(
    "/screen_analysis_agent/{user_id}/{screen_id}",
    response_model=ScreenAnalysisRecordResponse,
    summary="Get one screen analysis record",
    description="Return one screen analysis record identified by screen ID.",
)
async def get_screen_analysis_record(
    user_id: str,
    screen_id: str,
) -> ScreenAnalysisRecordResponse:
    """Return a single screen analysis record by ID."""
    decoded_id = parse_path_screen_id(screen_id)
    record = screen_analysis_agent_engine.get_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Screen analysis record not found",
        )

    return ScreenAnalysisRecordResponse.from_record(record)


@screen_analysis_agent_router.put(
    "/screen_analysis_agent/{user_id}/{screen_id}",
    response_model=ScreenAnalysisRecordResponse,
    status_code=status.HTTP_200_OK,
    summary="Update screen analysis record",
    description="Replace an existing screen analysis record with updated data.",
)
async def update_screen_analysis_record(
    user_id: str,
    screen_id: str,
    request: ScreenAnalysisRecord,
) -> ScreenAnalysisRecordResponse:
    """Update and return a screen analysis record."""
    decoded_id = parse_path_screen_id(screen_id)

    if normalize_screen_id(request.screen_id) != normalize_screen_id(decoded_id):
        if screen_analysis_agent_engine.screen_id_exists(user_id, request.screen_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Screen analysis record already exists",
            )

    record = screen_analysis_agent_engine.update_record(
        user_id,
        decoded_id,
        request,
    )
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Screen analysis record not found",
        )

    return ScreenAnalysisRecordResponse.from_record(record)


@screen_analysis_agent_router.delete(
    "/screen_analysis_agent/{user_id}/{screen_id}",
    response_model=ScreenAnalysisRecordResponse,
    summary="Delete screen analysis record",
    description="Delete a screen analysis record and return the removed record.",
)
async def delete_screen_analysis_record(
    user_id: str,
    screen_id: str,
) -> ScreenAnalysisRecordResponse:
    """Delete a screen analysis record and return the deleted item."""
    decoded_id = parse_path_screen_id(screen_id)
    record = screen_analysis_agent_engine.delete_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Screen analysis record not found",
        )

    return ScreenAnalysisRecordResponse.from_record(record)
