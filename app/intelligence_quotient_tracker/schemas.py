"""Pydantic schemas for the Intelligence Quotient Tracker Engine (Module 62)."""

from pydantic import BaseModel, ConfigDict, Field


class IntelligenceQuotientRecord(BaseModel):
    """Intelligence quotient record stored for a user."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "iq_id": "iq_001",
                    "iq_score": 128,
                    "classification": "Very Superior",
                    "test_date": "2026-06-04",
                }
            ]
        }
    )

    iq_id: str = Field(
        min_length=1,
        description="Unique IQ record identifier",
        examples=["iq_001"],
    )
    iq_score: int = Field(
        ge=0,
        description="Measured intelligence quotient score",
        examples=[128],
    )
    classification: str = Field(
        min_length=1,
        description="IQ score classification label",
        examples=["Very Superior"],
    )
    test_date: str = Field(
        min_length=1,
        description="Date the IQ test was taken",
        examples=["2026-06-04"],
    )


class IntelligenceQuotientRecordResponse(BaseModel):
    """Intelligence quotient record returned by the API."""

    iq_id: str
    iq_score: int
    classification: str
    test_date: str

    @classmethod
    def from_record(
        cls,
        record: IntelligenceQuotientRecord,
    ) -> "IntelligenceQuotientRecordResponse":
        """Build an API response from a stored IQ record."""
        return cls(
            iq_id=record.iq_id,
            iq_score=record.iq_score,
            classification=record.classification,
            test_date=record.test_date,
        )


class UserIntelligenceQuotientTrackerResponse(BaseModel):
    """All IQ records for one user."""

    user_id: str
    iq_records: list[IntelligenceQuotientRecordResponse]
