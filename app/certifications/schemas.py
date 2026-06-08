"""Pydantic schemas for the Certifications Service."""

from pydantic import BaseModel, Field


class Certification(BaseModel):
    """Certification record stored for a user."""

    name: str = Field(min_length=1, description="Certification name")
    organization: str = Field(min_length=1, description="Issuing organization")
    year: int = Field(ge=1900, description="Certification year (>= 1900)")


class CertificationResponse(BaseModel):
    """Certification record returned by the API."""

    name: str
    organization: str
    year: int

    @classmethod
    def from_certification(cls, certification: Certification) -> "CertificationResponse":
        """Build an API response from a stored certification record."""
        return cls(
            name=certification.name,
            organization=certification.organization,
            year=certification.year,
        )


class UserCertificationsResponse(BaseModel):
    """All certification records for one user."""

    user_id: str
    certifications: list[CertificationResponse]
