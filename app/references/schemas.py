"""Pydantic schemas for the References Service (Module 55)."""

from pydantic import BaseModel, ConfigDict, Field


class ReferenceRecord(BaseModel):
    """Professional reference record stored for a user."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "name": "Dr. Jane Smith",
                    "title": "Professor of AI",
                    "organization": "MIT",
                    "email": "jane.smith@mit.edu",
                }
            ]
        }
    )

    name: str = Field(
        min_length=1,
        description="Reference full name",
        examples=["Dr. Jane Smith"],
    )
    title: str = Field(
        min_length=1,
        description="Professional title or role",
        examples=["Professor of AI"],
    )
    organization: str = Field(
        min_length=1,
        description="Organization or institution",
        examples=["MIT"],
    )
    email: str = Field(
        min_length=1,
        description="Contact email address",
        examples=["jane.smith@mit.edu"],
    )


class ReferenceRecordResponse(BaseModel):
    """Reference record returned by the API."""

    name: str
    title: str
    organization: str
    email: str

    @classmethod
    def from_record(cls, record: ReferenceRecord) -> "ReferenceRecordResponse":
        """Build an API response from a stored reference record."""
        return cls(
            name=record.name,
            title=record.title,
            organization=record.organization,
            email=record.email,
        )


class UserReferencesResponse(BaseModel):
    """All reference records for one user."""

    user_id: str
    references: list[ReferenceRecordResponse]
