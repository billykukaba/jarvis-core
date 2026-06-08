"""FastAPI routes for the Projects Service."""

from fastapi import APIRouter, HTTPException, status

from app.projects.schemas import Project, ProjectResponse, UserProjectsResponse
from app.services.engine_registry import project_service_engine

# Router exposed to FastAPI as projects_router in main.py.
projects_router = APIRouter(tags=["projects"])


@projects_router.post(
    "/projects/{user_id}",
    response_model=ProjectResponse,
    summary="Create project record",
    description="Create a new project record for the specified user.",
)
async def create_project(user_id: str, request: Project) -> ProjectResponse:
    """Create and return a project record."""
    if project_service_engine.name_exists(user_id, request.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Project already exists",
        )

    project = project_service_engine.create_project(user_id, request)
    return ProjectResponse.from_project(project)


@projects_router.get(
    "/projects/{user_id}",
    response_model=UserProjectsResponse,
    summary="Get all project records",
    description="Return all project records saved by the specified user.",
)
async def get_projects(user_id: str) -> UserProjectsResponse:
    """Return all project records for a user."""
    projects = project_service_engine.get_projects(user_id)
    return UserProjectsResponse(
        user_id=user_id,
        projects=[ProjectResponse.from_project(project) for project in projects],
    )


@projects_router.get(
    "/projects/{user_id}/{name}",
    response_model=ProjectResponse,
    summary="Get one project record",
    description="Return one project record identified by name.",
)
async def get_project(user_id: str, name: str) -> ProjectResponse:
    """Return a single project record by name."""
    project = project_service_engine.get_project(user_id, name)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    return ProjectResponse.from_project(project)


@projects_router.put(
    "/projects/{user_id}/{name}",
    response_model=ProjectResponse,
    summary="Update project record",
    description="Replace an existing project record with updated data.",
)
async def update_project(
    user_id: str,
    name: str,
    request: Project,
) -> ProjectResponse:
    """Update and return a project record."""
    if (
        request.name.lower() != name.lower()
        and project_service_engine.name_exists(user_id, request.name)
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Project already exists",
        )

    project = project_service_engine.update_project(user_id, name, request)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    return ProjectResponse.from_project(project)


@projects_router.delete(
    "/projects/{user_id}/{name}",
    response_model=ProjectResponse,
    summary="Delete project record",
    description="Delete a project record and return the removed record.",
)
async def delete_project(user_id: str, name: str) -> ProjectResponse:
    """Delete a project record and return the deleted item."""
    project = project_service_engine.delete_project(user_id, name)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    return ProjectResponse.from_project(project)
