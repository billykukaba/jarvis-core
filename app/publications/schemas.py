"""Pydantic schemas for the Publications Service."""

from pydantic import BaseModel, Field


class Publication(BaseModel):
    """Publication record stored for a user."""

    title: str = Field(min_length=1, description="Publication title")
    publisher: str = Field(min_length=1, description="Publisher name")
    year: int = Field(ge=1900, description="Publication year (>= 1900)")


class PublicationResponse(BaseModel):
    """Publication record returned by the API."""

    title: str
    publisher: str
    year: int

    @classmethod
    def from_publication(cls, publication: Publication) -> "PublicationResponse":
        """Build an API response from a stored publication record."""
        return cls(
            title=publication.title,
            publisher=publication.publisher,
            year=publication.year,
        )


class UserPublicationsResponse(BaseModel):
    """All publication records for one user."""

    user_id: str
    publications: list[PublicationResponse]
