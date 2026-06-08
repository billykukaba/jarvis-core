from pydantic import BaseModel, Field

from app.project_memory.project_memory_engine import Project


class ProjectRequest(BaseModel):
    name: str = Field(min_length=1)
    description: str = Field(min_length=1)
    technologies: list[str]
    progress: str = Field(min_length=1)

    def to_project(self) -> Project:
        return Project(
            name=self.name,
            description=self.description,
            technologies=self.technologies,
            progress=self.progress,
        )


class ProjectResponse(BaseModel):
    name: str
    description: str
    technologies: list[str]
    progress: str

    @classmethod
    def from_project(cls, project: Project) -> "ProjectResponse":
        return cls(
            name=project.name,
            description=project.description,
            technologies=project.technologies,
            progress=project.progress,
        )


class UserProjectsResponse(BaseModel):
    user_id: str
    projects: list[ProjectResponse]
