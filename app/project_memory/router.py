from fastapi import APIRouter, HTTPException, status

from app.project_memory.schemas import (
    ProjectRequest,
    ProjectResponse,
    UserProjectsResponse,
)
from app.services.engine_registry import project_memory_engine

router = APIRouter(tags=["projects"])


@router.post("/projects/{user_id}", response_model=ProjectResponse)
async def add_project(user_id: str, request: ProjectRequest) -> ProjectResponse:
    project = project_memory_engine.add_project(user_id, request.to_project())
    return ProjectResponse.from_project(project)


@router.get("/projects/{user_id}", response_model=UserProjectsResponse)
async def get_projects(user_id: str) -> UserProjectsResponse:
    projects = project_memory_engine.get_projects(user_id)
    return UserProjectsResponse(
        user_id=user_id,
        projects=[ProjectResponse.from_project(project) for project in projects],
    )


@router.get("/projects/{user_id}/{project_name}", response_model=ProjectResponse)
async def get_project(user_id: str, project_name: str) -> ProjectResponse:
    project = project_memory_engine.get_project(user_id, project_name)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    return ProjectResponse.from_project(project)
