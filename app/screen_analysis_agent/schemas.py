"""Pydantic schemas for the Screen Analysis Agent."""

from pydantic import BaseModel, ConfigDict, Field


class ScreenAnalysisRecord(BaseModel):
    """Screen analysis record stored for a user."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "screen_id": "screen_001",
                    "screenshot_file": "desktop_capture.png",
                    "detected_application": "Visual Studio Code",
                    "screen_summary": "Developer workspace with code editor and terminal open.",
                    "detected_elements": ["editor", "sidebar", "terminal", "status_bar"],
                    "confidence_score": 92,
                    "status": "completed",
                    "progress_percentage": 100,
                    "created_at": "2026-06-04T09:00:00",
                    "updated_at": "2026-06-04T09:02:00",
                }
            ]
        }
    )

    screen_id: str = Field(
        min_length=1,
        description="Unique screen analysis record identifier",
        examples=["screen_001"],
    )
    screenshot_file: str = Field(
        min_length=1,
        description="Screenshot file name or path",
        examples=["desktop_capture.png"],
    )
    detected_application: str = Field(
        min_length=1,
        description="Primary application detected on screen",
        examples=["Visual Studio Code"],
    )
    screen_summary: str = Field(
        min_length=1,
        description="Natural language summary of the screen content",
        examples=["Developer workspace with code editor and terminal open."],
    )
    detected_elements: list[str] = Field(
        min_length=1,
        description="UI elements detected on the screen",
        examples=[["editor", "sidebar", "terminal", "status_bar"]],
    )
    confidence_score: int = Field(
        ge=0,
        le=100,
        description="Screen analysis confidence score",
        examples=[92],
    )
    status: str = Field(
        min_length=1,
        description="Current screen analysis status",
        examples=["completed"],
    )
    progress_percentage: int = Field(
        ge=0,
        le=100,
        description="Screen analysis progress percentage",
        examples=[100],
    )
    created_at: str = Field(
        min_length=1,
        description="Record creation timestamp",
        examples=["2026-06-04T09:00:00"],
    )
    updated_at: str = Field(
        min_length=1,
        description="Record last update timestamp",
        examples=["2026-06-04T09:02:00"],
    )


class ScreenAnalysisRecordResponse(BaseModel):
    """Screen analysis record returned by the API."""

    screen_id: str
    screenshot_file: str
    detected_application: str
    screen_summary: str
    detected_elements: list[str]
    confidence_score: int
    status: str
    progress_percentage: int
    created_at: str
    updated_at: str

    @classmethod
    def from_record(
        cls,
        record: ScreenAnalysisRecord,
    ) -> "ScreenAnalysisRecordResponse":
        """Build an API response from a stored screen analysis record."""
        return cls(
            screen_id=record.screen_id,
            screenshot_file=record.screenshot_file,
            detected_application=record.detected_application,
            screen_summary=record.screen_summary,
            detected_elements=record.detected_elements,
            confidence_score=record.confidence_score,
            status=record.status,
            progress_percentage=record.progress_percentage,
            created_at=record.created_at,
            updated_at=record.updated_at,
        )


class UserScreenAnalysisAgentResponse(BaseModel):
    """All screen analysis records for one user."""

    user_id: str
    screen_analysis_records: list[ScreenAnalysisRecordResponse]
