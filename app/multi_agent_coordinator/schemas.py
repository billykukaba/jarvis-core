"""Pydantic schemas for the Multi-Agent Coordinator."""

from pydantic import BaseModel, ConfigDict, Field


class MultiAgentCoordinatorRecord(BaseModel):
    """Multi-agent coordinator record stored for a user."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "coordinator_id": "coord_001",
                    "coordinator_name": "Research Squad",
                    "agents": ["analyst", "writer", "reviewer"],
                    "leader_agent": "analyst",
                    "current_task": "Draft quarterly report",
                    "priority_level": 2,
                    "status": "active",
                    "created_at": "2026-06-04T09:00:00",
                    "updated_at": "2026-06-04T10:30:00",
                }
            ]
        }
    )

    coordinator_id: str = Field(
        min_length=1,
        description="Unique coordinator identifier",
        examples=["coord_001"],
    )
    coordinator_name: str = Field(
        min_length=1,
        description="Display name of the coordinator group",
        examples=["Research Squad"],
    )
    agents: list[str] = Field(
        min_length=1,
        description="List of agent identifiers in the group",
        examples=[["analyst", "writer", "reviewer"]],
    )
    leader_agent: str = Field(
        min_length=1,
        description="Agent ID leading the coordinator group",
        examples=["analyst"],
    )
    current_task: str = Field(
        min_length=1,
        description="Task currently assigned to the group",
        examples=["Draft quarterly report"],
    )
    priority_level: int = Field(
        ge=0,
        description="Task priority level",
        examples=[2],
    )
    status: str = Field(
        min_length=1,
        description="Current coordinator status",
        examples=["active"],
    )
    created_at: str = Field(
        min_length=1,
        description="Coordinator creation timestamp",
        examples=["2026-06-04T09:00:00"],
    )
    updated_at: str = Field(
        min_length=1,
        description="Coordinator last update timestamp",
        examples=["2026-06-04T10:30:00"],
    )


class MultiAgentCoordinatorRecordResponse(BaseModel):
    """Multi-agent coordinator record returned by the API."""

    coordinator_id: str
    coordinator_name: str
    agents: list[str]
    leader_agent: str
    current_task: str
    priority_level: int
    status: str
    created_at: str
    updated_at: str

    @classmethod
    def from_record(
        cls,
        record: MultiAgentCoordinatorRecord,
    ) -> "MultiAgentCoordinatorRecordResponse":
        """Build an API response from a stored coordinator record."""
        return cls(
            coordinator_id=record.coordinator_id,
            coordinator_name=record.coordinator_name,
            agents=record.agents,
            leader_agent=record.leader_agent,
            current_task=record.current_task,
            priority_level=record.priority_level,
            status=record.status,
            created_at=record.created_at,
            updated_at=record.updated_at,
        )


class UserMultiAgentCoordinatorResponse(BaseModel):
    """All multi-agent coordinator records for one user."""

    user_id: str
    coordinators: list[MultiAgentCoordinatorRecordResponse]
