"""FastAPI routes for the Project Manager Agent."""

from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, status

from app.project_manager_agent.project_manager_agent_engine import (
    normalize_project_id,
)
from app.project_manager_agent.schemas import (
    ProjectRecord,
    ProjectRecordResponse,
    UserProjectManagerAgentResponse,
)
from app.services.engine_registry import project_manager_agent_engine

# Router exposed to FastAPI as project_manager_agent_router in main.py.
project_manager_agent_router = APIRouter(tags=["Project Manager Agent"])


def parse_path_project_id(project_id: str) -> str:
    """Decode URL path project IDs so spaces work in GET, PUT, and DELETE."""
    return unquote(project_id.replace("+", " "))


@project_manager_agent_router.post(
    "/project_manager_agent/{user_id}",
    response_model=ProjectRecordResponse,
    summary="Create project",
    description="Create a new project record for the specified user.",
)
async def create_project_record(
    user_id: str,
    request: ProjectRecord,
) -> ProjectRecordResponse:
    """Create and return a project record."""
    if project_manager_agent_engine.project_id_exists(user_id, request.project_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Project already exists",
        )

    record = project_manager_agent_engine.create_record(user_id, request)
    return ProjectRecordResponse.from_record(record)


@project_manager_agent_router.get(
    "/project_manager_agent/{user_id}",
    response_model=UserProjectManagerAgentResponse,
    summary="Get all projects",
    description="Return all project records saved by the specified user.",
)
async def get_project_records(user_id: str) -> UserProjectManagerAgentResponse:
    """Return all project records for a user."""
    records = project_manager_agent_engine.get_records(user_id)
    return UserProjectManagerAgentResponse(
        user_id=user_id,
        projects=[ProjectRecordResponse.from_record(record) for record in records],
    )


@project_manager_agent_router.get(
    "/project_manager_agent/{user_id}/{project_id}",
    response_model=ProjectRecordResponse,
    summary="Get one project",
    description="Return one project record identified by project ID.",
)
async def get_project_record(
    user_id: str,
    project_id: str,
) -> ProjectRecordResponse:
    """Return a single project record by ID."""
    decoded_id = parse_path_project_id(project_id)
    record = project_manager_agent_engine.get_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    return ProjectRecordResponse.from_record(record)


@project_manager_agent_router.put(
    "/project_manager_agent/{user_id}/{project_id}",
    response_model=ProjectRecordResponse,
    status_code=status.HTTP_200_OK,
    summary="Update project",
    description="Replace an existing project record with updated data.",
)
async def update_project_record(
    user_id: str,
    project_id: str,
    request: ProjectRecord,
) -> ProjectRecordResponse:
    """Update and return a project record."""
    decoded_id = parse_path_project_id(project_id)

    if normalize_project_id(request.project_id) != normalize_project_id(decoded_id):
        if project_manager_agent_engine.project_id_exists(user_id, request.project_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Project already exists",
            )

    record = project_manager_agent_engine.update_record(user_id, decoded_id, request)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    return ProjectRecordResponse.from_record(record)


@project_manager_agent_router.delete(
    "/project_manager_agent/{user_id}/{project_id}",
    response_model=ProjectRecordResponse,
    summary="Delete project",
    description="Delete a project record and return the removed record.",
)
async def delete_project_record(
    user_id: str,
    project_id: str,
) -> ProjectRecordResponse:
    """Delete a project record and return the deleted item."""
    decoded_id = parse_path_project_id(project_id)
    record = project_manager_agent_engine.delete_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    return ProjectRecordResponse.from_record(record)
