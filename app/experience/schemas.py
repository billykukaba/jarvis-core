"""Pydantic schemas for the Experience Service."""

from pydantic import BaseModel, Field, model_validator


class Experience(BaseModel):
    """Work experience record stored for a user."""

    company: str = Field(min_length=1, description="Employer or organization name")
    position: str = Field(min_length=1, description="Job title or role")
    start_year: int = Field(ge=1900, description="Start year (>= 1900)")
    end_year: int = Field(ge=1900, description="End year (>= start_year)")

    @model_validator(mode="after")
    def validate_years(self) -> "Experience":
        """Ensure end_year is not before start_year."""
        if self.end_year < self.start_year:
            raise ValueError("end_year must be greater than or equal to start_year")
        return self


class ExperienceResponse(BaseModel):
    """Experience record returned by the API."""

    company: str
    position: str
    start_year: int
    end_year: int

    @classmethod
    def from_experience(cls, experience: Experience) -> "ExperienceResponse":
        """Build an API response from a stored experience record."""
        return cls(
            company=experience.company,
            position=experience.position,
            start_year=experience.start_year,
            end_year=experience.end_year,
        )


class UserExperienceResponse(BaseModel):
    """All experience records for one user."""

    user_id: str
    experience: list[ExperienceResponse]
