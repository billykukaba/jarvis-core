"""Pydantic schemas for the Interests Service (Module 59)."""

from pydantic import BaseModel, ConfigDict, Field


class InterestRecord(BaseModel):
    """Personal interest record stored for a user."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "interest": "Machine Learning",
                    "level": "High",
                }
            ]
        }
    )

    interest: str = Field(
        min_length=1,
        description="Interest or hobby name",
        examples=["Machine Learning"],
    )
    level: str = Field(
        min_length=1,
        description="Interest level or intensity",
        examples=["High"],
    )


class InterestRecordResponse(BaseModel):
    """Interest record returned by the API."""

    interest: str
    level: str

    @classmethod
    def from_record(cls, record: InterestRecord) -> "InterestRecordResponse":
        """Build an API response from a stored interest record."""
        return cls(
            interest=record.interest,
            level=record.level,
        )


class UserInterestsResponse(BaseModel):
    """All interest records for one user."""

    user_id: str
    interests: list[InterestRecordResponse]
