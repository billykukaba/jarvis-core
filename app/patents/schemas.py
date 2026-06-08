"""Pydantic schemas for the Patents Service."""

from pydantic import BaseModel, Field


class Patent(BaseModel):
    """Patent record stored for a user."""

    title: str = Field(min_length=1, description="Patent title")
    patent_number: str = Field(min_length=1, description="Patent registration number")
    year: int = Field(ge=1900, description="Patent year (>= 1900)")


class PatentResponse(BaseModel):
    """Patent record returned by the API."""

    title: str
    patent_number: str
    year: int

    @classmethod
    def from_patent(cls, patent: Patent) -> "PatentResponse":
        """Build an API response from a stored patent record."""
        return cls(
            title=patent.title,
            patent_number=patent.patent_number,
            year=patent.year,
        )


class UserPatentsResponse(BaseModel):
    """All patent records for one user."""

    user_id: str
    patents: list[PatentResponse]
