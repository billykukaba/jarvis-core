"""FastAPI routes for the Website Automation Agent.

Automates interactions with websites including navigation, form filling, clicking,
data extraction and workflow execution for Jarvis Internet Intelligence.
"""

from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, status

from app.website_automation_agent.schemas import (
    UserWebsiteAutomationAgentResponse,
    WebsiteAutomationRecord,
    WebsiteAutomationRecordResponse,
)
from app.website_automation_agent.website_automation_agent_engine import (
    normalize_automation_id,
)
from app.services.engine_registry import website_automation_agent_engine

# Router exposed to FastAPI as website_automation_agent_router in main.py.
website_automation_agent_router = APIRouter(tags=["Website Automation Agent"])


def parse_path_automation_id(automation_id: str) -> str:
    """Decode URL path automation IDs so spaces work in GET, PUT, and DELETE."""
    return unquote(automation_id.replace("+", " "))


@website_automation_agent_router.post(
    "/website_automation_agent/{user_id}",
    response_model=WebsiteAutomationRecordResponse,
    summary="Create website automation",
    description=(
        "Create a new website automation record for the specified user. "
        "Automates interactions with websites including navigation, form filling, "
        "clicking, data extraction and workflow execution for Jarvis Internet "
        "Intelligence."
    ),
)
async def create_website_automation(
    user_id: str,
    request: WebsiteAutomationRecord,
) -> WebsiteAutomationRecordResponse:
    """Create and return a website automation record."""
    if website_automation_agent_engine.automation_id_exists(
        user_id,
        request.automation_id,
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Website automation already exists",
        )

    record = website_automation_agent_engine.create_record(user_id, request)
    return WebsiteAutomationRecordResponse.from_record(record)


@website_automation_agent_router.get(
    "/website_automation_agent/{user_id}",
    response_model=UserWebsiteAutomationAgentResponse,
    summary="Get all website automations",
    description=(
        "Return all website automation records saved by the specified user. "
        "Automates interactions with websites including navigation, form filling, "
        "clicking, data extraction and workflow execution for Jarvis Internet "
        "Intelligence."
    ),
)
async def get_website_automations(
    user_id: str,
) -> UserWebsiteAutomationAgentResponse:
    """Return all website automation records for a user."""
    records = website_automation_agent_engine.get_records(user_id)
    return UserWebsiteAutomationAgentResponse(
        user_id=user_id,
        website_automations=[
            WebsiteAutomationRecordResponse.from_record(record)
            for record in records
        ],
    )


@website_automation_agent_router.get(
    "/website_automation_agent/{user_id}/{automation_id}",
    response_model=WebsiteAutomationRecordResponse,
    summary="Get one website automation",
    description="Return one website automation record identified by automation ID.",
)
async def get_website_automation(
    user_id: str,
    automation_id: str,
) -> WebsiteAutomationRecordResponse:
    """Return a single website automation record by ID."""
    decoded_id = parse_path_automation_id(automation_id)
    record = website_automation_agent_engine.get_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Website automation not found",
        )

    return WebsiteAutomationRecordResponse.from_record(record)


@website_automation_agent_router.put(
    "/website_automation_agent/{user_id}/{automation_id}",
    response_model=WebsiteAutomationRecordResponse,
    status_code=status.HTTP_200_OK,
    summary="Update website automation",
    description="Replace an existing website automation record with updated data.",
)
async def update_website_automation(
    user_id: str,
    automation_id: str,
    request: WebsiteAutomationRecord,
) -> WebsiteAutomationRecordResponse:
    """Update and return a website automation record."""
    decoded_id = parse_path_automation_id(automation_id)

    if normalize_automation_id(request.automation_id) != normalize_automation_id(
        decoded_id,
    ):
        if website_automation_agent_engine.automation_id_exists(
            user_id,
            request.automation_id,
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Website automation already exists",
            )

    record = website_automation_agent_engine.update_record(
        user_id,
        decoded_id,
        request,
    )
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Website automation not found",
        )

    return WebsiteAutomationRecordResponse.from_record(record)


@website_automation_agent_router.delete(
    "/website_automation_agent/{user_id}/{automation_id}",
    response_model=WebsiteAutomationRecordResponse,
    summary="Delete website automation",
    description="Delete a website automation record and return the removed record.",
)
async def delete_website_automation(
    user_id: str,
    automation_id: str,
) -> WebsiteAutomationRecordResponse:
    """Delete a website automation record and return the deleted item."""
    decoded_id = parse_path_automation_id(automation_id)
    record = website_automation_agent_engine.delete_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Website automation not found",
        )

    return WebsiteAutomationRecordResponse.from_record(record)
