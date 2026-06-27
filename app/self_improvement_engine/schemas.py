"""Pydantic schemas for the Self Improvement Engine."""

from pydantic import BaseModel, ConfigDict, Field


class SelfImprovementRecord(BaseModel):
    """Self improvement record stored for a user."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "improvement_id": "improve_001",
                    "system_component": "response_generator",
                    "identified_problem": "Response latency increases under high load",
                    "proposed_solution": "Add response caching and async batch processing",
                    "expected_benefit": "Reduce average response time by 30%",
                    "priority_level": 85,
                    "implementation_status": "planned",
                    "confidence_score": 88,
                    "status": "active",
                    "progress_percentage": 25,
                    "created_at": "2026-06-05T00:00:00",
                    "updated_at": "2026-06-05T00:15:00",
                }
            ]
        }
    )

    improvement_id: str = Field(
        min_length=1,
        description="Unique self improvement record identifier",
        examples=["improve_001"],
    )
    system_component: str = Field(
        min_length=1,
        description="Jarvis system component targeted for improvement",
        examples=["response_generator"],
    )
    identified_problem: str = Field(
        min_length=1,
        description="Problem identified during performance analysis",
        examples=["Response latency increases under high load"],
    )
    proposed_solution: str = Field(
        min_length=1,
        description="Proposed solution for the identified problem",
        examples=["Add response caching and async batch processing"],
    )
    expected_benefit: str = Field(
        min_length=1,
        description="Expected benefit from implementing the solution",
        examples=["Reduce average response time by 30%"],
    )
    priority_level: int = Field(
        ge=0,
        le=100,
        description="Priority level of the improvement opportunity",
        examples=[85],
    )
    implementation_status: str = Field(
        min_length=1,
        description="Current implementation status of the improvement",
        examples=["planned"],
    )
    confidence_score: int = Field(
        ge=0,
        le=100,
        description="Confidence score for the improvement analysis",
        examples=[88],
    )
    status: str = Field(
        min_length=1,
        description="Current improvement record status",
        examples=["active"],
    )
    progress_percentage: int = Field(
        ge=0,
        le=100,
        description="Improvement progress percentage",
        examples=[25],
    )
    created_at: str = Field(
        min_length=1,
        description="Record creation timestamp",
        examples=["2026-06-05T00:00:00"],
    )
    updated_at: str = Field(
        min_length=1,
        description="Record last update timestamp",
        examples=["2026-06-05T00:15:00"],
    )


class SelfImprovementRecordResponse(BaseModel):
    """Self improvement record returned by the API."""

    improvement_id: str
    system_component: str
    identified_problem: str
    proposed_solution: str
    expected_benefit: str
    priority_level: int
    implementation_status: str
    confidence_score: int
    status: str
    progress_percentage: int
    created_at: str
    updated_at: str

    @classmethod
    def from_record(
        cls,
        record: SelfImprovementRecord,
    ) -> "SelfImprovementRecordResponse":
        """Build an API response from a stored self improvement record."""
        return cls(
            improvement_id=record.improvement_id,
            system_component=record.system_component,
            identified_problem=record.identified_problem,
            proposed_solution=record.proposed_solution,
            expected_benefit=record.expected_benefit,
            priority_level=record.priority_level,
            implementation_status=record.implementation_status,
            confidence_score=record.confidence_score,
            status=record.status,
            progress_percentage=record.progress_percentage,
            created_at=record.created_at,
            updated_at=record.updated_at,
        )


class UserSelfImprovementEngineResponse(BaseModel):
    """All self improvement records for one user."""

    user_id: str
    improvement_records: list[SelfImprovementRecordResponse]
