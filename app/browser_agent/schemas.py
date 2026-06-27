"""Pydantic schemas for the Browser Agent."""

from pydantic import BaseModel, ConfigDict, Field


class BrowserSessionRecord(BaseModel):
    """Browser session record stored for a user."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "browser_session_id": "session_001",
                    "website_url": "https://docs.python.org/3/",
                    "page_title": "Python 3 Documentation",
                    "page_summary": "Official Python language reference and tutorials.",
                    "visited_pages": [
                        "https://docs.python.org/3/",
                        "https://docs.python.org/3/tutorial/",
                    ],
                    "search_query": "python documentation",
                    "browser_status": "active",
                    "confidence_score": 94,
                    "progress_percentage": 100,
                    "created_at": "2026-06-04T18:00:00",
                    "updated_at": "2026-06-04T18:10:00",
                }
            ]
        }
    )

    browser_session_id: str = Field(
        min_length=1,
        description="Unique browser session record identifier",
        examples=["session_001"],
    )
    website_url: str = Field(
        min_length=1,
        description="Primary website URL for the browser session",
        examples=["https://docs.python.org/3/"],
    )
    page_title: str = Field(
        min_length=1,
        description="Title of the current or primary page",
        examples=["Python 3 Documentation"],
    )
    page_summary: str = Field(
        min_length=1,
        description="Summary of the page content",
        examples=["Official Python language reference and tutorials."],
    )
    visited_pages: list[str] = Field(
        min_length=1,
        description="List of URLs visited during the session",
        examples=[
            [
                "https://docs.python.org/3/",
                "https://docs.python.org/3/tutorial/",
            ]
        ],
    )
    search_query: str = Field(
        min_length=1,
        description="Search query associated with the browser session",
        examples=["python documentation"],
    )
    browser_status: str = Field(
        min_length=1,
        description="Current browser session status",
        examples=["active"],
    )
    confidence_score: int = Field(
        ge=0,
        le=100,
        description="Browser session analysis confidence score",
        examples=[94],
    )
    progress_percentage: int = Field(
        ge=0,
        le=100,
        description="Browser session progress percentage",
        examples=[100],
    )
    created_at: str = Field(
        min_length=1,
        description="Record creation timestamp",
        examples=["2026-06-04T18:00:00"],
    )
    updated_at: str = Field(
        min_length=1,
        description="Record last update timestamp",
        examples=["2026-06-04T18:10:00"],
    )


class BrowserSessionRecordResponse(BaseModel):
    """Browser session record returned by the API."""

    browser_session_id: str
    website_url: str
    page_title: str
    page_summary: str
    visited_pages: list[str]
    search_query: str
    browser_status: str
    confidence_score: int
    progress_percentage: int
    created_at: str
    updated_at: str

    @classmethod
    def from_record(
        cls,
        record: BrowserSessionRecord,
    ) -> "BrowserSessionRecordResponse":
        """Build an API response from a stored browser session record."""
        return cls(
            browser_session_id=record.browser_session_id,
            website_url=record.website_url,
            page_title=record.page_title,
            page_summary=record.page_summary,
            visited_pages=record.visited_pages,
            search_query=record.search_query,
            browser_status=record.browser_status,
            confidence_score=record.confidence_score,
            progress_percentage=record.progress_percentage,
            created_at=record.created_at,
            updated_at=record.updated_at,
        )


class UserBrowserAgentResponse(BaseModel):
    """All browser session records for one user."""

    user_id: str
    browser_sessions: list[BrowserSessionRecordResponse]
