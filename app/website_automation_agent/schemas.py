"""Pydantic schemas for the Website Automation Agent."""

from pydantic import BaseModel, ConfigDict, Field


class WebsiteAutomationRecord(BaseModel):
    """Website automation record stored for a user."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "automation_id": "auto_001",
                    "website_url": "https://example.com/login",
                    "automation_name": "Daily Login Flow",
                    "automation_type": "form_submission",
                    "trigger_action": "scheduled_daily",
                    "execution_steps": [
                        "navigate to login page",
                        "fill username field",
                        "fill password field",
                        "click submit button",
                    ],
                    "execution_result": "Login completed successfully",
                    "execution_status": "completed",
                    "success_rate": 98,
                    "progress_percentage": 100,
                    "created_at": "2026-06-04T20:00:00",
                    "updated_at": "2026-06-04T20:05:00",
                }
            ]
        }
    )

    automation_id: str = Field(
        min_length=1,
        description="Unique website automation record identifier",
        examples=["auto_001"],
    )
    website_url: str = Field(
        min_length=1,
        description="Target website URL for the automation",
        examples=["https://example.com/login"],
    )
    automation_name: str = Field(
        min_length=1,
        description="Name of the website automation workflow",
        examples=["Daily Login Flow"],
    )
    automation_type: str = Field(
        min_length=1,
        description="Type of automation workflow",
        examples=["form_submission"],
    )
    trigger_action: str = Field(
        min_length=1,
        description="Action that triggers the automation",
        examples=["scheduled_daily"],
    )
    execution_steps: list[str] = Field(
        min_length=1,
        description="Ordered steps executed by the automation",
        examples=[
            [
                "navigate to login page",
                "fill username field",
                "fill password field",
                "click submit button",
            ]
        ],
    )
    execution_result: str = Field(
        min_length=1,
        description="Result of the automation execution",
        examples=["Login completed successfully"],
    )
    execution_status: str = Field(
        min_length=1,
        description="Current execution status of the automation",
        examples=["completed"],
    )
    success_rate: int = Field(
        ge=0,
        le=100,
        description="Success rate percentage of the automation",
        examples=[98],
    )
    progress_percentage: int = Field(
        ge=0,
        le=100,
        description="Automation progress percentage",
        examples=[100],
    )
    created_at: str = Field(
        min_length=1,
        description="Record creation timestamp",
        examples=["2026-06-04T20:00:00"],
    )
    updated_at: str = Field(
        min_length=1,
        description="Record last update timestamp",
        examples=["2026-06-04T20:05:00"],
    )


class WebsiteAutomationRecordResponse(BaseModel):
    """Website automation record returned by the API."""

    automation_id: str
    website_url: str
    automation_name: str
    automation_type: str
    trigger_action: str
    execution_steps: list[str]
    execution_result: str
    execution_status: str
    success_rate: int
    progress_percentage: int
    created_at: str
    updated_at: str

    @classmethod
    def from_record(
        cls,
        record: WebsiteAutomationRecord,
    ) -> "WebsiteAutomationRecordResponse":
        """Build an API response from a stored website automation record."""
        return cls(
            automation_id=record.automation_id,
            website_url=record.website_url,
            automation_name=record.automation_name,
            automation_type=record.automation_type,
            trigger_action=record.trigger_action,
            execution_steps=record.execution_steps,
            execution_result=record.execution_result,
            execution_status=record.execution_status,
            success_rate=record.success_rate,
            progress_percentage=record.progress_percentage,
            created_at=record.created_at,
            updated_at=record.updated_at,
        )


class UserWebsiteAutomationAgentResponse(BaseModel):
    """All website automation records for one user."""

    user_id: str
    website_automations: list[WebsiteAutomationRecordResponse]
