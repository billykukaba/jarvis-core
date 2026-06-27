"""FastAPI routes for the Browser Agent.

Manages browser sessions, visited websites, searches and browsing history
for Jarvis Internet Intelligence.
"""

from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, status

from app.browser_agent.browser_agent_engine import normalize_browser_session_id
from app.browser_agent.schemas import (
    BrowserSessionRecord,
    BrowserSessionRecordResponse,
    UserBrowserAgentResponse,
)
from app.services.engine_registry import browser_agent_engine

# Router exposed to FastAPI as browser_agent_router in main.py.
browser_agent_router = APIRouter(tags=["Browser Agent"])


def parse_path_browser_session_id(browser_session_id: str) -> str:
    """Decode URL path browser session IDs so spaces work in GET, PUT, and DELETE."""
    return unquote(browser_session_id.replace("+", " "))


@browser_agent_router.post(
    "/browser_agent/{user_id}",
    response_model=BrowserSessionRecordResponse,
    summary="Create browser session",
    description=(
        "Create a new browser session record for the specified user. "
        "Manages browser sessions, visited websites, searches and browsing "
        "history for Jarvis Internet Intelligence."
    ),
)
async def create_browser_session(
    user_id: str,
    request: BrowserSessionRecord,
) -> BrowserSessionRecordResponse:
    """Create and return a browser session record."""
    if browser_agent_engine.browser_session_id_exists(
        user_id,
        request.browser_session_id,
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Browser session already exists",
        )

    record = browser_agent_engine.create_record(user_id, request)
    return BrowserSessionRecordResponse.from_record(record)


@browser_agent_router.get(
    "/browser_agent/{user_id}",
    response_model=UserBrowserAgentResponse,
    summary="Get all browser sessions",
    description=(
        "Return all browser session records saved by the specified user. "
        "Manages browser sessions, visited websites, searches and browsing "
        "history for Jarvis Internet Intelligence."
    ),
)
async def get_browser_sessions(
    user_id: str,
) -> UserBrowserAgentResponse:
    """Return all browser session records for a user."""
    records = browser_agent_engine.get_records(user_id)
    return UserBrowserAgentResponse(
        user_id=user_id,
        browser_sessions=[
            BrowserSessionRecordResponse.from_record(record) for record in records
        ],
    )


@browser_agent_router.get(
    "/browser_agent/{user_id}/{browser_session_id}",
    response_model=BrowserSessionRecordResponse,
    summary="Get one browser session",
    description="Return one browser session record identified by session ID.",
)
async def get_browser_session(
    user_id: str,
    browser_session_id: str,
) -> BrowserSessionRecordResponse:
    """Return a single browser session record by ID."""
    decoded_id = parse_path_browser_session_id(browser_session_id)
    record = browser_agent_engine.get_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Browser session not found",
        )

    return BrowserSessionRecordResponse.from_record(record)


@browser_agent_router.put(
    "/browser_agent/{user_id}/{browser_session_id}",
    response_model=BrowserSessionRecordResponse,
    status_code=status.HTTP_200_OK,
    summary="Update browser session",
    description="Replace an existing browser session record with updated data.",
)
async def update_browser_session(
    user_id: str,
    browser_session_id: str,
    request: BrowserSessionRecord,
) -> BrowserSessionRecordResponse:
    """Update and return a browser session record."""
    decoded_id = parse_path_browser_session_id(browser_session_id)

    if normalize_browser_session_id(
        request.browser_session_id,
    ) != normalize_browser_session_id(decoded_id):
        if browser_agent_engine.browser_session_id_exists(
            user_id,
            request.browser_session_id,
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Browser session already exists",
            )

    record = browser_agent_engine.update_record(
        user_id,
        decoded_id,
        request,
    )
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Browser session not found",
        )

    return BrowserSessionRecordResponse.from_record(record)


@browser_agent_router.delete(
    "/browser_agent/{user_id}/{browser_session_id}",
    response_model=BrowserSessionRecordResponse,
    summary="Delete browser session",
    description="Delete a browser session record and return the removed record.",
)
async def delete_browser_session(
    user_id: str,
    browser_session_id: str,
) -> BrowserSessionRecordResponse:
    """Delete a browser session record and return the deleted item."""
    decoded_id = parse_path_browser_session_id(browser_session_id)
    record = browser_agent_engine.delete_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Browser session not found",
        )

    return BrowserSessionRecordResponse.from_record(record)
