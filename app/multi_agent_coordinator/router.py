"""FastAPI routes for the Multi-Agent Coordinator."""

from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, status

from app.multi_agent_coordinator.multi_agent_coordinator_engine import (
    normalize_coordinator_id,
)
from app.multi_agent_coordinator.schemas import (
    MultiAgentCoordinatorRecord,
    MultiAgentCoordinatorRecordResponse,
    UserMultiAgentCoordinatorResponse,
)
from app.services.engine_registry import multi_agent_coordinator_engine

# Router exposed to FastAPI as multi_agent_coordinator_router in main.py.
multi_agent_coordinator_router = APIRouter(tags=["Multi-Agent Coordinator"])


def parse_path_coordinator_id(coordinator_id: str) -> str:
    """Decode URL path coordinator IDs so spaces work in GET, PUT, and DELETE."""
    return unquote(coordinator_id.replace("+", " "))


@multi_agent_coordinator_router.post(
    "/multi_agent_coordinator/{user_id}",
    response_model=MultiAgentCoordinatorRecordResponse,
    summary="Create coordinator",
    description="Create a new multi-agent coordinator record for the specified user.",
)
async def create_coordinator_record(
    user_id: str,
    request: MultiAgentCoordinatorRecord,
) -> MultiAgentCoordinatorRecordResponse:
    """Create and return a coordinator record."""
    if multi_agent_coordinator_engine.coordinator_id_exists(
        user_id,
        request.coordinator_id,
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Coordinator already exists",
        )

    record = multi_agent_coordinator_engine.create_record(user_id, request)
    return MultiAgentCoordinatorRecordResponse.from_record(record)


@multi_agent_coordinator_router.get(
    "/multi_agent_coordinator/{user_id}",
    response_model=UserMultiAgentCoordinatorResponse,
    summary="Get all coordinators",
    description="Return all multi-agent coordinator records saved by the specified user.",
)
async def get_coordinator_records(
    user_id: str,
) -> UserMultiAgentCoordinatorResponse:
    """Return all coordinator records for a user."""
    records = multi_agent_coordinator_engine.get_records(user_id)
    return UserMultiAgentCoordinatorResponse(
        user_id=user_id,
        coordinators=[
            MultiAgentCoordinatorRecordResponse.from_record(record)
            for record in records
        ],
    )


@multi_agent_coordinator_router.get(
    "/multi_agent_coordinator/{user_id}/{coordinator_id}",
    response_model=MultiAgentCoordinatorRecordResponse,
    summary="Get one coordinator",
    description="Return one multi-agent coordinator record identified by coordinator ID.",
)
async def get_coordinator_record(
    user_id: str,
    coordinator_id: str,
) -> MultiAgentCoordinatorRecordResponse:
    """Return a single coordinator record by ID."""
    decoded_id = parse_path_coordinator_id(coordinator_id)
    record = multi_agent_coordinator_engine.get_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coordinator not found",
        )

    return MultiAgentCoordinatorRecordResponse.from_record(record)


@multi_agent_coordinator_router.put(
    "/multi_agent_coordinator/{user_id}/{coordinator_id}",
    response_model=MultiAgentCoordinatorRecordResponse,
    status_code=status.HTTP_200_OK,
    summary="Update coordinator",
    description="Replace an existing multi-agent coordinator record with updated data.",
)
async def update_coordinator_record(
    user_id: str,
    coordinator_id: str,
    request: MultiAgentCoordinatorRecord,
) -> MultiAgentCoordinatorRecordResponse:
    """Update and return a coordinator record."""
    decoded_id = parse_path_coordinator_id(coordinator_id)

    if normalize_coordinator_id(request.coordinator_id) != normalize_coordinator_id(
        decoded_id
    ):
        if multi_agent_coordinator_engine.coordinator_id_exists(
            user_id,
            request.coordinator_id,
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Coordinator already exists",
            )

    record = multi_agent_coordinator_engine.update_record(
        user_id,
        decoded_id,
        request,
    )
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coordinator not found",
        )

    return MultiAgentCoordinatorRecordResponse.from_record(record)


@multi_agent_coordinator_router.delete(
    "/multi_agent_coordinator/{user_id}/{coordinator_id}",
    response_model=MultiAgentCoordinatorRecordResponse,
    summary="Delete coordinator",
    description="Delete a multi-agent coordinator record and return the removed record.",
)
async def delete_coordinator_record(
    user_id: str,
    coordinator_id: str,
) -> MultiAgentCoordinatorRecordResponse:
    """Delete a coordinator record and return the deleted item."""
    decoded_id = parse_path_coordinator_id(coordinator_id)
    record = multi_agent_coordinator_engine.delete_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coordinator not found",
        )

    return MultiAgentCoordinatorRecordResponse.from_record(record)
