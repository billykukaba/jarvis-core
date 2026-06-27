"""FastAPI routes for the News Monitoring Agent.

Monitors news sources, tracks articles, categories and priorities
for Jarvis Internet Intelligence.
"""

from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, status

from app.news_monitoring_agent.news_monitoring_agent_engine import normalize_news_id
from app.news_monitoring_agent.schemas import (
    NewsMonitoringRecord,
    NewsMonitoringRecordResponse,
    UserNewsMonitoringAgentResponse,
)
from app.services.engine_registry import news_monitoring_agent_engine

# Router exposed to FastAPI as news_monitoring_agent_router in main.py.
news_monitoring_agent_router = APIRouter(tags=["News Monitoring Agent"])


def parse_path_news_id(news_id: str) -> str:
    """Decode URL path news IDs so spaces work in GET, PUT, and DELETE."""
    return unquote(news_id.replace("+", " "))


@news_monitoring_agent_router.post(
    "/news_monitoring_agent/{user_id}",
    response_model=NewsMonitoringRecordResponse,
    summary="Create news monitoring record",
    description=(
        "Create a new news monitoring record for the specified user. "
        "Monitors news sources, tracks articles, categories and priorities "
        "for Jarvis Internet Intelligence."
    ),
)
async def create_news_monitoring_record(
    user_id: str,
    request: NewsMonitoringRecord,
) -> NewsMonitoringRecordResponse:
    """Create and return a news monitoring record."""
    if news_monitoring_agent_engine.news_id_exists(user_id, request.news_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="News monitoring record already exists",
        )

    record = news_monitoring_agent_engine.create_record(user_id, request)
    return NewsMonitoringRecordResponse.from_record(record)


@news_monitoring_agent_router.get(
    "/news_monitoring_agent/{user_id}",
    response_model=UserNewsMonitoringAgentResponse,
    summary="Get all news monitoring records",
    description=(
        "Return all news monitoring records saved by the specified user. "
        "Monitors news sources, tracks articles, categories and priorities "
        "for Jarvis Internet Intelligence."
    ),
)
async def get_news_monitoring_records(
    user_id: str,
) -> UserNewsMonitoringAgentResponse:
    """Return all news monitoring records for a user."""
    records = news_monitoring_agent_engine.get_records(user_id)
    return UserNewsMonitoringAgentResponse(
        user_id=user_id,
        news_records=[
            NewsMonitoringRecordResponse.from_record(record) for record in records
        ],
    )


@news_monitoring_agent_router.get(
    "/news_monitoring_agent/{user_id}/{news_id}",
    response_model=NewsMonitoringRecordResponse,
    summary="Get one news monitoring record",
    description="Return one news monitoring record identified by news ID.",
)
async def get_news_monitoring_record(
    user_id: str,
    news_id: str,
) -> NewsMonitoringRecordResponse:
    """Return a single news monitoring record by ID."""
    decoded_id = parse_path_news_id(news_id)
    record = news_monitoring_agent_engine.get_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="News monitoring record not found",
        )

    return NewsMonitoringRecordResponse.from_record(record)


@news_monitoring_agent_router.put(
    "/news_monitoring_agent/{user_id}/{news_id}",
    response_model=NewsMonitoringRecordResponse,
    status_code=status.HTTP_200_OK,
    summary="Update news monitoring record",
    description="Replace an existing news monitoring record with updated data.",
)
async def update_news_monitoring_record(
    user_id: str,
    news_id: str,
    request: NewsMonitoringRecord,
) -> NewsMonitoringRecordResponse:
    """Update and return a news monitoring record."""
    decoded_id = parse_path_news_id(news_id)

    if normalize_news_id(request.news_id) != normalize_news_id(decoded_id):
        if news_monitoring_agent_engine.news_id_exists(user_id, request.news_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="News monitoring record already exists",
            )

    record = news_monitoring_agent_engine.update_record(
        user_id,
        decoded_id,
        request,
    )
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="News monitoring record not found",
        )

    return NewsMonitoringRecordResponse.from_record(record)


@news_monitoring_agent_router.delete(
    "/news_monitoring_agent/{user_id}/{news_id}",
    response_model=NewsMonitoringRecordResponse,
    summary="Delete news monitoring record",
    description="Delete a news monitoring record and return the removed record.",
)
async def delete_news_monitoring_record(
    user_id: str,
    news_id: str,
) -> NewsMonitoringRecordResponse:
    """Delete a news monitoring record and return the deleted item."""
    decoded_id = parse_path_news_id(news_id)
    record = news_monitoring_agent_engine.delete_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="News monitoring record not found",
        )

    return NewsMonitoringRecordResponse.from_record(record)
