"""Pydantic schemas for the Research Service (Module 53)."""

from pydantic import BaseModel, ConfigDict, Field


class ResearchRecord(BaseModel):
    """Research record stored for a user."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "title": "Neural Network Optimization",
                    "institution": "MIT CSAIL",
                    "year": 2033,
                }
            ]
        }
    )

    title: str = Field(
        min_length=1,
        description="Research project or paper title",
        examples=["Neural Network Optimization"],
    )
    institution: str = Field(
        min_length=1,
        description="Research institution or lab",
        examples=["MIT CSAIL"],
    )
    year: int = Field(
        ge=1900,
        description="Research year (>= 1900)",
        examples=[2033],
    )


class ResearchRecordResponse(BaseModel):
    """Research record returned by the API."""

    title: str
    institution: str
    year: int

    @classmethod
    def from_record(cls, record: ResearchRecord) -> "ResearchRecordResponse":
        """Build an API response from a stored research record."""
        return cls(
            title=record.title,
            institution=record.institution,
            year=record.year,
        )


class UserResearchResponse(BaseModel):
    """All research records for one user."""

    user_id: str
    research: list[ResearchRecordResponse]
