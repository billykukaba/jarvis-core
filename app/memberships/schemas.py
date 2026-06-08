"""Pydantic schemas for the Memberships Service (Module 56)."""

from pydantic import BaseModel, ConfigDict, Field


class MembershipRecord(BaseModel):
    """Professional membership record stored for a user."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "organization": "IEEE",
                    "role": "Senior Member",
                    "year": 2032,
                }
            ]
        }
    )

    organization: str = Field(
        min_length=1,
        description="Professional organization name",
        examples=["IEEE"],
    )
    role: str = Field(
        min_length=1,
        description="Membership role or level",
        examples=["Senior Member"],
    )
    year: int = Field(
        ge=1900,
        description="Membership year (>= 1900)",
        examples=[2032],
    )


class MembershipRecordResponse(BaseModel):
    """Membership record returned by the API."""

    organization: str
    role: str
    year: int

    @classmethod
    def from_record(cls, record: MembershipRecord) -> "MembershipRecordResponse":
        """Build an API response from a stored membership record."""
        return cls(
            organization=record.organization,
            role=record.role,
            year=record.year,
        )


class UserMembershipsResponse(BaseModel):
    """All membership records for one user."""

    user_id: str
    memberships: list[MembershipRecordResponse]
