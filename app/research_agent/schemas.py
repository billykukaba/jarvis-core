"""Pydantic schemas for the Research Agent."""

from pydantic import BaseModel, ConfigDict, Field


class ResearchRecord(BaseModel):
    """Research record stored for a user."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "research_id": "res_001",
                    "research_topic": "AI Safety Trends",
                    "description": "Survey recent developments in AI safety research",
                    "sources": [
                        "https://example.com/paper-a",
                        "https://example.com/report-b",
                    ],
                    "findings": [
                        "Increased focus on alignment",
                        "Growing regulatory interest",
                    ],
                    "reliability_score": 85,
                    "status": "in_progress",
                    "progress_percentage": 60,
                    "created_at": "2026-06-04T09:00:00",
                    "updated_at": "2026-06-04T10:30:00",
                }
            ]
        }
    )

    research_id: str = Field(
        min_length=1,
        description="Unique research identifier",
        examples=["res_001"],
    )
    research_topic: str = Field(
        min_length=1,
        description="Topic being researched",
        examples=["AI Safety Trends"],
    )
    description: str = Field(
        min_length=1,
        description="Detailed research description",
        examples=["Survey recent developments in AI safety research"],
    )
    sources: list[str] = Field(
        min_length=1,
        description="List of research sources",
        examples=[
            [
                "https://example.com/paper-a",
                "https://example.com/report-b",
            ]
        ],
    )
    findings: list[str] = Field(
        min_length=1,
        description="List of research findings",
        examples=[
            [
                "Increased focus on alignment",
                "Growing regulatory interest",
            ]
        ],
    )
    reliability_score: int = Field(
        ge=0,
        le=100,
        description="Reliability score of the research",
        examples=[85],
    )
    status: str = Field(
        min_length=1,
        description="Current research status",
        examples=["in_progress"],
    )
    progress_percentage: int = Field(
        ge=0,
        le=100,
        description="Research completion percentage",
        examples=[60],
    )
    created_at: str = Field(
        min_length=1,
        description="Research creation timestamp",
        examples=["2026-06-04T09:00:00"],
    )
    updated_at: str = Field(
        min_length=1,
        description="Research last update timestamp",
        examples=["2026-06-04T10:30:00"],
    )


class ResearchRecordResponse(BaseModel):
    """Research record returned by the API."""

    research_id: str
    research_topic: str
    description: str
    sources: list[str]
    findings: list[str]
    reliability_score: int
    status: str
    progress_percentage: int
    created_at: str
    updated_at: str

    @classmethod
    def from_record(cls, record: ResearchRecord) -> "ResearchRecordResponse":
        """Build an API response from a stored research record."""
        return cls(
            research_id=record.research_id,
            research_topic=record.research_topic,
            description=record.description,
            sources=record.sources,
            findings=record.findings,
            reliability_score=record.reliability_score,
            status=record.status,
            progress_percentage=record.progress_percentage,
            created_at=record.created_at,
            updated_at=record.updated_at,
        )


class UserResearchAgentResponse(BaseModel):
    """All research records for one user."""

    user_id: str
    research_records: list[ResearchRecordResponse]
