"""Pydantic schemas for the News Monitoring Agent."""

from pydantic import BaseModel, ConfigDict, Field


class NewsMonitoringRecord(BaseModel):
    """News monitoring record stored for a user."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "news_id": "news_001",
                    "news_title": "AI Breakthrough in Language Models",
                    "news_source": "Tech Daily",
                    "news_category": "technology",
                    "news_summary": "Researchers announce major advances in multilingual AI models.",
                    "news_url": "https://example.com/ai-breakthrough",
                    "published_date": "2026-06-04",
                    "keywords": ["AI", "language models", "research"],
                    "priority_level": 8,
                    "status": "monitored",
                    "progress_percentage": 100,
                    "created_at": "2026-06-04T19:00:00",
                    "updated_at": "2026-06-04T19:05:00",
                }
            ]
        }
    )

    news_id: str = Field(
        min_length=1,
        description="Unique news monitoring record identifier",
        examples=["news_001"],
    )
    news_title: str = Field(
        min_length=1,
        description="Title of the news article",
        examples=["AI Breakthrough in Language Models"],
    )
    news_source: str = Field(
        min_length=1,
        description="Source of the news article",
        examples=["Tech Daily"],
    )
    news_category: str = Field(
        min_length=1,
        description="Category classification of the news article",
        examples=["technology"],
    )
    news_summary: str = Field(
        min_length=1,
        description="Summary of the news article content",
        examples=["Researchers announce major advances in multilingual AI models."],
    )
    news_url: str = Field(
        min_length=1,
        description="URL of the news article",
        examples=["https://example.com/ai-breakthrough"],
    )
    published_date: str = Field(
        min_length=1,
        description="Publication date of the news article",
        examples=["2026-06-04"],
    )
    keywords: list[str] = Field(
        min_length=1,
        description="Keywords associated with the news article",
        examples=[["AI", "language models", "research"]],
    )
    priority_level: int = Field(
        ge=0,
        le=100,
        description="Priority level of the news monitoring record",
        examples=[8],
    )
    status: str = Field(
        min_length=1,
        description="Current news monitoring status",
        examples=["monitored"],
    )
    progress_percentage: int = Field(
        ge=0,
        le=100,
        description="News monitoring progress percentage",
        examples=[100],
    )
    created_at: str = Field(
        min_length=1,
        description="Record creation timestamp",
        examples=["2026-06-04T19:00:00"],
    )
    updated_at: str = Field(
        min_length=1,
        description="Record last update timestamp",
        examples=["2026-06-04T19:05:00"],
    )


class NewsMonitoringRecordResponse(BaseModel):
    """News monitoring record returned by the API."""

    news_id: str
    news_title: str
    news_source: str
    news_category: str
    news_summary: str
    news_url: str
    published_date: str
    keywords: list[str]
    priority_level: int
    status: str
    progress_percentage: int
    created_at: str
    updated_at: str

    @classmethod
    def from_record(
        cls,
        record: NewsMonitoringRecord,
    ) -> "NewsMonitoringRecordResponse":
        """Build an API response from a stored news monitoring record."""
        return cls(
            news_id=record.news_id,
            news_title=record.news_title,
            news_source=record.news_source,
            news_category=record.news_category,
            news_summary=record.news_summary,
            news_url=record.news_url,
            published_date=record.published_date,
            keywords=record.keywords,
            priority_level=record.priority_level,
            status=record.status,
            progress_percentage=record.progress_percentage,
            created_at=record.created_at,
            updated_at=record.updated_at,
        )


class UserNewsMonitoringAgentResponse(BaseModel):
    """All news monitoring records for one user."""

    user_id: str
    news_records: list[NewsMonitoringRecordResponse]
