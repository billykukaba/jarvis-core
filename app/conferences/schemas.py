"""Pydantic schemas for the Conferences Service (Module 54)."""

from pydantic import BaseModel, ConfigDict, Field


class ConferenceRecord(BaseModel):
    """Conference record stored for a user."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "title": "AI Summit Keynote",
                    "event": "MIT AI Conference",
                    "year": 2033,
                }
            ]
        }
    )

    title: str = Field(
        min_length=1,
        description="Presentation or talk title",
        examples=["AI Summit Keynote"],
    )
    event: str = Field(
        min_length=1,
        description="Conference or event name",
        examples=["MIT AI Conference"],
    )
    year: int = Field(
        ge=1900,
        description="Conference year (>= 1900)",
        examples=[2033],
    )


class ConferenceRecordResponse(BaseModel):
    """Conference record returned by the API."""

    title: str
    event: str
    year: int

    @classmethod
    def from_record(cls, record: ConferenceRecord) -> "ConferenceRecordResponse":
        """Build an API response from a stored conference record."""
        return cls(
            title=record.title,
            event=record.event,
            year=record.year,
        )


class UserConferencesResponse(BaseModel):
    """All conference records for one user."""

    user_id: str
    conferences: list[ConferenceRecordResponse]
