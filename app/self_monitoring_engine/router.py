"""FastAPI routes for the Self Monitoring Engine.

Monitors Jarvis internal components, health status, issues, risks and recommended actions.
"""

from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, status

from app.self_monitoring_engine.schemas import (
    SelfMonitoringRecord,
    SelfMonitoringRecordResponse,
    UserSelfMonitoringEngineResponse,
)
from app.self_monitoring_engine.self_monitoring_engine_engine import (
    normalize_monitoring_id,
)
from app.services.engine_registry import self_monitoring_engine

# Router exposed to FastAPI as self_monitoring_engine_router in main.py.
self_monitoring_engine_router = APIRouter(tags=["Self Monitoring Engine"])


def parse_path_monitoring_id(monitoring_id: str) -> str:
    """Decode URL path monitoring IDs so spaces work in GET, PUT, and DELETE."""
    return unquote(monitoring_id.replace("+", " "))


@self_monitoring_engine_router.post(
    "/self_monitoring_engine/{user_id}",
    response_model=SelfMonitoringRecordResponse,
    summary="Create monitoring record",
    description=(
        "Create a new self monitoring record for the specified user. "
        "Monitors Jarvis internal components, health status, issues, risks "
        "and recommended actions."
    ),
)
async def create_self_monitoring_record(
    user_id: str,
    request: SelfMonitoringRecord,
) -> SelfMonitoringRecordResponse:
    """Create and return a self monitoring record."""
    if self_monitoring_engine.monitoring_id_exists(user_id, request.monitoring_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Monitoring record already exists",
        )

    record = self_monitoring_engine.create_record(user_id, request)
    return SelfMonitoringRecordResponse.from_record(record)


@self_monitoring_engine_router.get(
    "/self_monitoring_engine/{user_id}",
    response_model=UserSelfMonitoringEngineResponse,
    summary="Get all monitoring records",
    description=(
        "Return all self monitoring records saved by the specified user. "
        "Monitors Jarvis internal components, health status, issues, risks "
        "and recommended actions."
    ),
)
async def get_self_monitoring_records(
    user_id: str,
) -> UserSelfMonitoringEngineResponse:
    """Return all self monitoring records for a user."""
    records = self_monitoring_engine.get_records(user_id)
    return UserSelfMonitoringEngineResponse(
        user_id=user_id,
        monitoring_records=[
            SelfMonitoringRecordResponse.from_record(record) for record in records
        ],
    )


@self_monitoring_engine_router.get(
    "/self_monitoring_engine/{user_id}/{monitoring_id}",
    response_model=SelfMonitoringRecordResponse,
    summary="Get one monitoring record",
    description="Return one self monitoring record identified by monitoring ID.",
)
async def get_self_monitoring_record(
    user_id: str,
    monitoring_id: str,
) -> SelfMonitoringRecordResponse:
    """Return a single self monitoring record by ID."""
    decoded_id = parse_path_monitoring_id(monitoring_id)
    record = self_monitoring_engine.get_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Monitoring record not found",
        )

    return SelfMonitoringRecordResponse.from_record(record)


@self_monitoring_engine_router.put(
    "/self_monitoring_engine/{user_id}/{monitoring_id}",
    response_model=SelfMonitoringRecordResponse,
    status_code=status.HTTP_200_OK,
    summary="Update monitoring record",
    description="Replace an existing self monitoring record with updated data.",
)
async def update_self_monitoring_record(
    user_id: str,
    monitoring_id: str,
    request: SelfMonitoringRecord,
) -> SelfMonitoringRecordResponse:
    """Update and return a self monitoring record."""
    decoded_id = parse_path_monitoring_id(monitoring_id)

    if normalize_monitoring_id(request.monitoring_id) != normalize_monitoring_id(
        decoded_id,
    ):
        if self_monitoring_engine.monitoring_id_exists(user_id, request.monitoring_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Monitoring record already exists",
            )

    record = self_monitoring_engine.update_record(
        user_id,
        decoded_id,
        request,
    )
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Monitoring record not found",
        )

    return SelfMonitoringRecordResponse.from_record(record)


@self_monitoring_engine_router.delete(
    "/self_monitoring_engine/{user_id}/{monitoring_id}",
    response_model=SelfMonitoringRecordResponse,
    summary="Delete monitoring record",
    description="Delete a self monitoring record and return the removed record.",
)
async def delete_self_monitoring_record(
    user_id: str,
    monitoring_id: str,
) -> SelfMonitoringRecordResponse:
    """Delete a self monitoring record and return the deleted item."""
    decoded_id = parse_path_monitoring_id(monitoring_id)
    record = self_monitoring_engine.delete_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Monitoring record not found",
        )

    return SelfMonitoringRecordResponse.from_record(record)
