"""Pydantic schemas for the Project Manager Agent."""

from pydantic import BaseModel, ConfigDict, Field


class ProjectRecord(BaseModel):
    """Project record stored for a user."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "project_id": "proj_001",
                    "project_name": "Website Redesign",
                    "description": "Redesign the company website for improved UX",
                    "objectives": [
                        "Audit current site",
                        "Design new layout",
                        "Launch updated site",
                    ],
                    "team_members": ["alice", "bob", "carol"],
                    "status": "in_progress",
                    "priority_level": 1,
                    "completion_percentage": 35,
                    "deadline": "2026-08-01",
                    "created_at": "2026-06-04T09:00:00",
                    "updated_at": "2026-06-04T10:30:00",
                }
            ]
        }
    )

    project_id: str = Field(
        min_length=1,
        description="Unique project identifier",
        examples=["proj_001"],
    )
    project_name: str = Field(
        min_length=1,
        description="Display name of the project",
        examples=["Website Redesign"],
    )
    description: str = Field(
        min_length=1,
        description="Detailed project description",
        examples=["Redesign the company website for improved UX"],
    )
    objectives: list[str] = Field(
        min_length=1,
        description="List of project objectives",
        examples=[["Audit current site", "Design new layout", "Launch updated site"]],
    )
    team_members: list[str] = Field(
        min_length=1,
        description="List of team member identifiers",
        examples=[["alice", "bob", "carol"]],
    )
    status: str = Field(
        min_length=1,
        description="Current project status",
        examples=["in_progress"],
    )
    priority_level: int = Field(
        ge=0,
        description="Project priority level",
        examples=[1],
    )
    completion_percentage: int = Field(
        ge=0,
        le=100,
        description="Project completion percentage",
        examples=[35],
    )
    deadline: str = Field(
        min_length=1,
        description="Project deadline date",
        examples=["2026-08-01"],
    )
    created_at: str = Field(
        min_length=1,
        description="Project creation timestamp",
        examples=["2026-06-04T09:00:00"],
    )
    updated_at: str = Field(
        min_length=1,
        description="Project last update timestamp",
        examples=["2026-06-04T10:30:00"],
    )


class ProjectRecordResponse(BaseModel):
    """Project record returned by the API."""

    project_id: str
    project_name: str
    description: str
    objectives: list[str]
    team_members: list[str]
    status: str
    priority_level: int
    completion_percentage: int
    deadline: str
    created_at: str
    updated_at: str

    @classmethod
    def from_record(cls, record: ProjectRecord) -> "ProjectRecordResponse":
        """Build an API response from a stored project record."""
        return cls(
            project_id=record.project_id,
            project_name=record.project_name,
            description=record.description,
            objectives=record.objectives,
            team_members=record.team_members,
            status=record.status,
            priority_level=record.priority_level,
            completion_percentage=record.completion_percentage,
            deadline=record.deadline,
            created_at=record.created_at,
            updated_at=record.updated_at,
        )


class UserProjectManagerAgentResponse(BaseModel):
    """All project records for one user."""

    user_id: str
    projects: list[ProjectRecordResponse]
