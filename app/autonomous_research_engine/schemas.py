"""Pydantic schemas for the Autonomous Research Engine."""

from pydantic import BaseModel, ConfigDict, Field


class AutonomousResearchRecord(BaseModel):
    """Autonomous research record stored for a user."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "research_id": "research_001",
                    "research_goal": "Analyze emerging AI regulation trends",
                    "research_topic": "AI policy",
                    "research_plan": "Scan news, browse official sources, summarize findings",
                    "used_agents": [
                        "browser_agent",
                        "news_monitoring_agent",
                        "website_automation_agent",
                    ],
                    "visited_sources": [
                        "https://example.com/ai-policy",
                        "https://news.example.com/ai-regulation",
                    ],
                    "research_summary": "Global AI regulation is accelerating across major regions.",
                    "final_conclusion": "Compliance frameworks are becoming mandatory within 24 months.",
                    "confidence_score": 91,
                    "status": "completed",
                    "progress_percentage": 100,
                    "created_at": "2026-06-04T21:00:00",
                    "updated_at": "2026-06-04T21:30:00",
                }
            ]
        }
    )

    research_id: str = Field(
        min_length=1,
        description="Unique autonomous research record identifier",
        examples=["research_001"],
    )
    research_goal: str = Field(
        min_length=1,
        description="Primary goal of the research mission",
        examples=["Analyze emerging AI regulation trends"],
    )
    research_topic: str = Field(
        min_length=1,
        description="Topic area of the research mission",
        examples=["AI policy"],
    )
    research_plan: str = Field(
        min_length=1,
        description="Planned approach for executing the research mission",
        examples=["Scan news, browse official sources, summarize findings"],
    )
    used_agents: list[str] = Field(
        min_length=1,
        description="Jarvis agents used during the research mission",
        examples=[
            [
                "browser_agent",
                "news_monitoring_agent",
                "website_automation_agent",
            ]
        ],
    )
    visited_sources: list[str] = Field(
        min_length=1,
        description="Sources visited during the research mission",
        examples=[
            [
                "https://example.com/ai-policy",
                "https://news.example.com/ai-regulation",
            ]
        ],
    )
    research_summary: str = Field(
        min_length=1,
        description="Summary of research findings",
        examples=["Global AI regulation is accelerating across major regions."],
    )
    final_conclusion: str = Field(
        min_length=1,
        description="Final conclusion of the research mission",
        examples=[
            "Compliance frameworks are becoming mandatory within 24 months."
        ],
    )
    confidence_score: int = Field(
        ge=0,
        le=100,
        description="Research mission confidence score",
        examples=[91],
    )
    status: str = Field(
        min_length=1,
        description="Current research mission status",
        examples=["completed"],
    )
    progress_percentage: int = Field(
        ge=0,
        le=100,
        description="Research mission progress percentage",
        examples=[100],
    )
    created_at: str = Field(
        min_length=1,
        description="Record creation timestamp",
        examples=["2026-06-04T21:00:00"],
    )
    updated_at: str = Field(
        min_length=1,
        description="Record last update timestamp",
        examples=["2026-06-04T21:30:00"],
    )


class AutonomousResearchRecordResponse(BaseModel):
    """Autonomous research record returned by the API."""

    research_id: str
    research_goal: str
    research_topic: str
    research_plan: str
    used_agents: list[str]
    visited_sources: list[str]
    research_summary: str
    final_conclusion: str
    confidence_score: int
    status: str
    progress_percentage: int
    created_at: str
    updated_at: str

    @classmethod
    def from_record(
        cls,
        record: AutonomousResearchRecord,
    ) -> "AutonomousResearchRecordResponse":
        """Build an API response from a stored autonomous research record."""
        return cls(
            research_id=record.research_id,
            research_goal=record.research_goal,
            research_topic=record.research_topic,
            research_plan=record.research_plan,
            used_agents=record.used_agents,
            visited_sources=record.visited_sources,
            research_summary=record.research_summary,
            final_conclusion=record.final_conclusion,
            confidence_score=record.confidence_score,
            status=record.status,
            progress_percentage=record.progress_percentage,
            created_at=record.created_at,
            updated_at=record.updated_at,
        )


class UserAutonomousResearchEngineResponse(BaseModel):
    """All autonomous research records for one user."""

    user_id: str
    research_records: list[AutonomousResearchRecordResponse]
