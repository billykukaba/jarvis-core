"""Pydantic schemas for the Workflow Engine."""

from pydantic import BaseModel, ConfigDict, Field


class WorkflowRecord(BaseModel):
    """Workflow record stored for a user."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "workflow_id": "wf_001",
                    "workflow_name": "Onboarding Pipeline",
                    "description": "Standard new-hire onboarding workflow",
                    "steps": [
                        "Create account",
                        "Assign mentor",
                        "Complete training",
                    ],
                    "status": "in_progress",
                    "progress_percentage": 33.3,
                    "created_at": "2026-06-04T09:00:00",
                    "updated_at": "2026-06-04T10:30:00",
                }
            ]
        }
    )

    workflow_id: str = Field(
        min_length=1,
        description="Unique workflow identifier",
        examples=["wf_001"],
    )
    workflow_name: str = Field(
        min_length=1,
        description="Display name of the workflow",
        examples=["Onboarding Pipeline"],
    )
    description: str = Field(
        min_length=1,
        description="Workflow description",
        examples=["Standard new-hire onboarding workflow"],
    )
    steps: list[str] = Field(
        min_length=1,
        description="Ordered list of workflow steps",
        examples=[["Create account", "Assign mentor", "Complete training"]],
    )
    status: str = Field(
        min_length=1,
        description="Current workflow status",
        examples=["in_progress"],
    )
    progress_percentage: float = Field(
        ge=0,
        le=100,
        description="Workflow completion percentage",
        examples=[33.3],
    )
    created_at: str = Field(
        min_length=1,
        description="Workflow creation timestamp",
        examples=["2026-06-04T09:00:00"],
    )
    updated_at: str = Field(
        min_length=1,
        description="Workflow last update timestamp",
        examples=["2026-06-04T10:30:00"],
    )


class WorkflowRecordResponse(BaseModel):
    """Workflow record returned by the API."""

    workflow_id: str
    workflow_name: str
    description: str
    steps: list[str]
    status: str
    progress_percentage: float
    created_at: str
    updated_at: str

    @classmethod
    def from_record(cls, record: WorkflowRecord) -> "WorkflowRecordResponse":
        """Build an API response from a stored workflow record."""
        return cls(
            workflow_id=record.workflow_id,
            workflow_name=record.workflow_name,
            description=record.description,
            steps=record.steps,
            status=record.status,
            progress_percentage=record.progress_percentage,
            created_at=record.created_at,
            updated_at=record.updated_at,
        )


class UserWorkflowEngineResponse(BaseModel):
    """All workflow records for one user."""

    user_id: str
    workflows: list[WorkflowRecordResponse]
