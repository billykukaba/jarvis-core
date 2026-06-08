"""Pydantic schemas for the Projects Service."""

from pydantic import BaseModel, Field


class Project(BaseModel):
    """Project record stored for a user."""

    name: str = Field(min_length=1, description="Project name")
    description: str = Field(min_length=1, description="Project description")
    year: int = Field(ge=1900, description="Project year (>= 1900)")


class ProjectResponse(BaseModel):
    """Project record returned by the API."""

    name: str
    description: str
    year: int

    @classmethod
    def from_project(cls, project: Project) -> "ProjectResponse":
        """Build an API response from a stored project record."""
        return cls(
            name=project.name,
            description=project.description,
            year=project.year,
        )


class UserProjectsResponse(BaseModel):
    """All project records for one user."""

    user_id: str
    projects: list[ProjectResponse]
