"""Pydantic schemas for the Licenses Service (Module 57)."""

from pydantic import BaseModel, ConfigDict, Field


class LicenseRecord(BaseModel):
    """Professional license record stored for a user."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "name": "Professional Engineer License",
                    "issuer": "Massachusetts Board",
                    "year": 2032,
                }
            ]
        }
    )

    name: str = Field(
        min_length=1,
        description="License name or type",
        examples=["Professional Engineer License"],
    )
    issuer: str = Field(
        min_length=1,
        description="Issuing authority or board",
        examples=["Massachusetts Board"],
    )
    year: int = Field(
        ge=1900,
        description="License year (>= 1900)",
        examples=[2032],
    )


class LicenseRecordResponse(BaseModel):
    """License record returned by the API."""

    name: str
    issuer: str
    year: int

    @classmethod
    def from_record(cls, record: LicenseRecord) -> "LicenseRecordResponse":
        """Build an API response from a stored license record."""
        return cls(
            name=record.name,
            issuer=record.issuer,
            year=record.year,
        )


class UserLicensesResponse(BaseModel):
    """All license records for one user."""

    user_id: str
    licenses: list[LicenseRecordResponse]
