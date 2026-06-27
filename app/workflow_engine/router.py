"""FastAPI routes for the Workflow Engine."""

from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, status

from app.services.engine_registry import workflow_engine
from app.workflow_engine.schemas import (
    UserWorkflowEngineResponse,
    WorkflowRecord,
    WorkflowRecordResponse,
)
from app.workflow_engine.workflow_engine import normalize_workflow_id

# Router exposed to FastAPI as workflow_engine_router in main.py.
workflow_engine_router = APIRouter(tags=["Workflow Engine"])


def parse_path_workflow_id(workflow_id: str) -> str:
    """Decode URL path workflow IDs so spaces work in GET, PUT, and DELETE."""
    return unquote(workflow_id.replace("+", " "))


@workflow_engine_router.post(
    "/workflow_engine/{user_id}",
    response_model=WorkflowRecordResponse,
    summary="Create workflow",
    description="Create a new workflow record for the specified user.",
)
async def create_workflow_record(
    user_id: str,
    request: WorkflowRecord,
) -> WorkflowRecordResponse:
    """Create and return a workflow record."""
    if workflow_engine.workflow_id_exists(user_id, request.workflow_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Workflow already exists",
        )

    record = workflow_engine.create_record(user_id, request)
    return WorkflowRecordResponse.from_record(record)


@workflow_engine_router.get(
    "/workflow_engine/{user_id}",
    response_model=UserWorkflowEngineResponse,
    summary="Get all workflows",
    description="Return all workflow records saved by the specified user.",
)
async def get_workflow_records(user_id: str) -> UserWorkflowEngineResponse:
    """Return all workflow records for a user."""
    records = workflow_engine.get_records(user_id)
    return UserWorkflowEngineResponse(
        user_id=user_id,
        workflows=[
            WorkflowRecordResponse.from_record(record) for record in records
        ],
    )


@workflow_engine_router.get(
    "/workflow_engine/{user_id}/{workflow_id}",
    response_model=WorkflowRecordResponse,
    summary="Get one workflow",
    description="Return one workflow record identified by workflow ID.",
)
async def get_workflow_record(
    user_id: str,
    workflow_id: str,
) -> WorkflowRecordResponse:
    """Return a single workflow record by ID."""
    decoded_id = parse_path_workflow_id(workflow_id)
    record = workflow_engine.get_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workflow not found",
        )

    return WorkflowRecordResponse.from_record(record)


@workflow_engine_router.put(
    "/workflow_engine/{user_id}/{workflow_id}",
    response_model=WorkflowRecordResponse,
    status_code=status.HTTP_200_OK,
    summary="Update workflow",
    description="Replace an existing workflow record with updated data.",
)
async def update_workflow_record(
    user_id: str,
    workflow_id: str,
    request: WorkflowRecord,
) -> WorkflowRecordResponse:
    """Update and return a workflow record."""
    decoded_id = parse_path_workflow_id(workflow_id)

    if normalize_workflow_id(request.workflow_id) != normalize_workflow_id(decoded_id):
        if workflow_engine.workflow_id_exists(user_id, request.workflow_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Workflow already exists",
            )

    record = workflow_engine.update_record(user_id, decoded_id, request)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workflow not found",
        )

    return WorkflowRecordResponse.from_record(record)


@workflow_engine_router.delete(
    "/workflow_engine/{user_id}/{workflow_id}",
    response_model=WorkflowRecordResponse,
    summary="Delete workflow",
    description="Delete a workflow record and return the removed record.",
)
async def delete_workflow_record(
    user_id: str,
    workflow_id: str,
) -> WorkflowRecordResponse:
    """Delete a workflow record and return the deleted item."""
    decoded_id = parse_path_workflow_id(workflow_id)
    record = workflow_engine.delete_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workflow not found",
        )

    return WorkflowRecordResponse.from_record(record)
