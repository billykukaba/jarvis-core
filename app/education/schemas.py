"""Pydantic schemas for the Education Service."""

from pydantic import BaseModel, Field, model_validator


class EducationRecord(BaseModel):
    """Education record stored for a user."""

    institution: str = Field(min_length=1, description="School or university name")
    degree: str = Field(min_length=1, description="Degree or program name")
    field: str = Field(min_length=1, description="Field of study")
    start_year: int = Field(ge=1900, description="Start year (>= 1900)")
    end_year: int = Field(ge=1900, description="End year (>= start_year)")

    @model_validator(mode="after")
    def validate_years(self) -> "EducationRecord":
        """Ensure end_year is not before start_year."""
        if self.end_year < self.start_year:
            raise ValueError("end_year must be greater than or equal to start_year")
        return self


class EducationRecordResponse(BaseModel):
    """Education record returned by the API."""

    institution: str
    degree: str
    field: str
    start_year: int
    end_year: int

    @classmethod
    def from_record(cls, record: EducationRecord) -> "EducationRecordResponse":
        """Build an API response from a stored education record."""
        return cls(
            institution=record.institution,
            degree=record.degree,
            field=record.field,
            start_year=record.start_year,
            end_year=record.end_year,
        )


class UserEducationResponse(BaseModel):
    """All education records for one user."""

    user_id: str
    education: list[EducationRecordResponse]
