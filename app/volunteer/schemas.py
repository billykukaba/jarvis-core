"""Pydantic schemas for the Volunteer Service (Module 52)."""

from pydantic import BaseModel, ConfigDict, Field


class VolunteerRecord(BaseModel):
    """Volunteer experience record stored for a user."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "organization": "MIT OpenCourseWare",
                    "role": "Content Contributor",
                    "year": 2032,
                }
            ]
        }
    )

    organization: str = Field(
        min_length=1,
        description="Volunteer organization name",
        examples=["MIT OpenCourseWare"],
    )
    role: str = Field(
        min_length=1,
        description="Volunteer role or contribution",
        examples=["Content Contributor"],
    )
    year: int = Field(
        ge=1900,
        description="Year of volunteer activity (>= 1900)",
        examples=[2032],
    )


class VolunteerRecordResponse(BaseModel):
    """Volunteer record returned by the API."""

    organization: str
    role: str
    year: int

    @classmethod
    def from_record(cls, record: VolunteerRecord) -> "VolunteerRecordResponse":
        """Build an API response from a stored volunteer record."""
        return cls(
            organization=record.organization,
            role=record.role,
            year=record.year,
        )


class UserVolunteerResponse(BaseModel):
    """All volunteer records for one user."""

    user_id: str
    volunteer: list[VolunteerRecordResponse]
