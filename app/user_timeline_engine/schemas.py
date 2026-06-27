"""Pydantic schemas for the User Timeline Engine."""

from pydantic import BaseModel, ConfigDict, Field


class UserTimelineRecord(BaseModel):
    """User timeline record stored for a user."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "timeline_id": "timeline_001",
                    "event_title": "Jarvis Core MVP Completed",
                    "event_description": "Completed the first MVP release of Jarvis Core.",
                    "event_category": "project_milestone",
                    "event_date": "2026-06-05",
                    "related_project": "jarvis_core",
                    "importance_score": 92,
                    "status": "completed",
                    "progress_percentage": 100,
                    "created_at": "2026-06-05T05:00:00",
                    "updated_at": "2026-06-05T05:10:00",
                }
            ]
        }
    )

    timeline_id: str = Field(
        min_length=1,
        description="Unique user timeline record identifier",
        examples=["timeline_001"],
    )
    event_title: str = Field(
        min_length=1,
        description="Title of the timeline event",
        examples=["Jarvis Core MVP Completed"],
    )
    event_description: str = Field(
        min_length=1,
        description="Description of the timeline event",
        examples=["Completed the first MVP release of Jarvis Core."],
    )
    event_category: str = Field(
        min_length=1,
        description="Category classification of the timeline event",
        examples=["project_milestone"],
    )
    event_date: str = Field(
        min_length=1,
        description="Date of the timeline event",
        examples=["2026-06-05"],
    )
    related_project: str = Field(
        min_length=1,
        description="Project related to the timeline event",
        examples=["jarvis_core"],
    )
    importance_score: int = Field(
        ge=0,
        le=100,
        description="Importance score of the timeline event",
        examples=[92],
    )
    status: str = Field(
        min_length=1,
        description="Current timeline record status",
        examples=["completed"],
    )
    progress_percentage: int = Field(
        ge=0,
        le=100,
        description="Timeline record progress percentage",
        examples=[100],
    )
    created_at: str = Field(
        min_length=1,
        description="Record creation timestamp",
        examples=["2026-06-05T05:00:00"],
    )
    updated_at: str = Field(
        min_length=1,
        description="Record last update timestamp",
        examples=["2026-06-05T05:10:00"],
    )


class UserTimelineRecordResponse(BaseModel):
    """User timeline record returned by the API."""

    timeline_id: str
    event_title: str
    event_description: str
    event_category: str
    event_date: str
    related_project: str
    importance_score: int
    status: str
    progress_percentage: int
    created_at: str
    updated_at: str

    @classmethod
    def from_record(
        cls,
        record: UserTimelineRecord,
    ) -> "UserTimelineRecordResponse":
        """Build an API response from a stored user timeline record."""
        return cls(
            timeline_id=record.timeline_id,
            event_title=record.event_title,
            event_description=record.event_description,
            event_category=record.event_category,
            event_date=record.event_date,
            related_project=record.related_project,
            importance_score=record.importance_score,
            status=record.status,
            progress_percentage=record.progress_percentage,
            created_at=record.created_at,
            updated_at=record.updated_at,
        )


class UserTimelineEngineResponse(BaseModel):
    """All user timeline records for one user."""

    user_id: str
    timeline_records: list[UserTimelineRecordResponse]
