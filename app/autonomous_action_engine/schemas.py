"""Pydantic schemas for the Autonomous Action Engine."""

from pydantic import BaseModel, ConfigDict, Field


class AutonomousActionRecord(BaseModel):
    """Autonomous action record stored for a user."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "action_id": "action_001",
                    "action_goal": "Deploy updated configuration to staging",
                    "action_type": "system_deployment",
                    "target_system": "staging_environment",
                    "required_tools": ["workflow_engine", "website_automation_agent"],
                    "execution_plan": [
                        "validate configuration",
                        "run pre-deployment checks",
                        "apply configuration",
                        "verify deployment status",
                    ],
                    "execution_result": "Configuration deployed successfully",
                    "risk_level": 35,
                    "approval_required": True,
                    "status": "completed",
                    "progress_percentage": 100,
                    "created_at": "2026-06-04T22:00:00",
                    "updated_at": "2026-06-04T22:15:00",
                }
            ]
        }
    )

    action_id: str = Field(
        min_length=1,
        description="Unique autonomous action record identifier",
        examples=["action_001"],
    )
    action_goal: str = Field(
        min_length=1,
        description="Primary goal of the autonomous action",
        examples=["Deploy updated configuration to staging"],
    )
    action_type: str = Field(
        min_length=1,
        description="Type classification of the autonomous action",
        examples=["system_deployment"],
    )
    target_system: str = Field(
        min_length=1,
        description="Target system for the autonomous action",
        examples=["staging_environment"],
    )
    required_tools: list[str] = Field(
        min_length=1,
        description="Tools required to execute the autonomous action",
        examples=[["workflow_engine", "website_automation_agent"]],
    )
    execution_plan: list[str] = Field(
        min_length=1,
        description="Ordered steps in the execution plan",
        examples=[
            [
                "validate configuration",
                "run pre-deployment checks",
                "apply configuration",
                "verify deployment status",
            ]
        ],
    )
    execution_result: str = Field(
        min_length=1,
        description="Result of the autonomous action execution",
        examples=["Configuration deployed successfully"],
    )
    risk_level: int = Field(
        ge=0,
        le=100,
        description="Risk level associated with the autonomous action",
        examples=[35],
    )
    approval_required: bool = Field(
        description="Whether manual approval is required before execution",
        examples=[True],
    )
    status: str = Field(
        min_length=1,
        description="Current autonomous action status",
        examples=["completed"],
    )
    progress_percentage: int = Field(
        ge=0,
        le=100,
        description="Autonomous action progress percentage",
        examples=[100],
    )
    created_at: str = Field(
        min_length=1,
        description="Record creation timestamp",
        examples=["2026-06-04T22:00:00"],
    )
    updated_at: str = Field(
        min_length=1,
        description="Record last update timestamp",
        examples=["2026-06-04T22:15:00"],
    )


class AutonomousActionRecordResponse(BaseModel):
    """Autonomous action record returned by the API."""

    action_id: str
    action_goal: str
    action_type: str
    target_system: str
    required_tools: list[str]
    execution_plan: list[str]
    execution_result: str
    risk_level: int
    approval_required: bool
    status: str
    progress_percentage: int
    created_at: str
    updated_at: str

    @classmethod
    def from_record(
        cls,
        record: AutonomousActionRecord,
    ) -> "AutonomousActionRecordResponse":
        """Build an API response from a stored autonomous action record."""
        return cls(
            action_id=record.action_id,
            action_goal=record.action_goal,
            action_type=record.action_type,
            target_system=record.target_system,
            required_tools=record.required_tools,
            execution_plan=record.execution_plan,
            execution_result=record.execution_result,
            risk_level=record.risk_level,
            approval_required=record.approval_required,
            status=record.status,
            progress_percentage=record.progress_percentage,
            created_at=record.created_at,
            updated_at=record.updated_at,
        )


class UserAutonomousActionEngineResponse(BaseModel):
    """All autonomous action records for one user."""

    user_id: str
    autonomous_actions: list[AutonomousActionRecordResponse]
