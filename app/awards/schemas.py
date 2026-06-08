"""Pydantic schemas for the Awards Service."""

from pydantic import BaseModel, Field


class Award(BaseModel):
    """Award record stored for a user."""

    title: str = Field(min_length=1, description="Award title")
    issuer: str = Field(min_length=1, description="Issuing organization")
    year: int = Field(ge=1900, description="Year the award was received (>= 1900)")


class AwardResponse(BaseModel):
    """Award record returned by the API."""

    title: str
    issuer: str
    year: int

    @classmethod
    def from_award(cls, award: Award) -> "AwardResponse":
        """Build an API response from a stored award record."""
        return cls(
            title=award.title,
            issuer=award.issuer,
            year=award.year,
        )


class UserAwardsResponse(BaseModel):
    """All award records for one user."""

    user_id: str
    awards: list[AwardResponse]
