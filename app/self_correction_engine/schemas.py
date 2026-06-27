"""Pydantic schemas for the Self Correction Engine."""

from pydantic import BaseModel, ConfigDict, Field


class SelfCorrectionRecord(BaseModel):
    """Self correction record stored for a user."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "correction_id": "corr_001",
                    "error_source": "reasoning_engine",
                    "error_description": "Incorrect date calculation in response",
                    "correction_strategy": "Re-run reasoning with validated date context",
                    "corrected_output": "The event occurs on June 15, 2026, not June 5.",
                    "confidence_score": 94,
                    "correction_status": "applied",
                    "status": "completed",
                    "progress_percentage": 100,
                    "created_at": "2026-06-05T02:00:00",
                    "updated_at": "2026-06-05T02:10:00",
                }
            ]
        }
    )

    correction_id: str = Field(
        min_length=1,
        description="Unique self correction record identifier",
        examples=["corr_001"],
    )
    error_source: str = Field(
        min_length=1,
        description="Source component where the error originated",
        examples=["reasoning_engine"],
    )
    error_description: str = Field(
        min_length=1,
        description="Description of the detected error",
        examples=["Incorrect date calculation in response"],
    )
    correction_strategy: str = Field(
        min_length=1,
        description="Strategy used to correct the error",
        examples=["Re-run reasoning with validated date context"],
    )
    corrected_output: str = Field(
        min_length=1,
        description="Output produced after applying the correction",
        examples=["The event occurs on June 15, 2026, not June 5."],
    )
    confidence_score: int = Field(
        ge=0,
        le=100,
        description="Confidence score for the correction",
        examples=[94],
    )
    correction_status: str = Field(
        min_length=1,
        description="Status of the correction process",
        examples=["applied"],
    )
    status: str = Field(
        min_length=1,
        description="Current correction record status",
        examples=["completed"],
    )
    progress_percentage: int = Field(
        ge=0,
        le=100,
        description="Correction progress percentage",
        examples=[100],
    )
    created_at: str = Field(
        min_length=1,
        description="Record creation timestamp",
        examples=["2026-06-05T02:00:00"],
    )
    updated_at: str = Field(
        min_length=1,
        description="Record last update timestamp",
        examples=["2026-06-05T02:10:00"],
    )


class SelfCorrectionRecordResponse(BaseModel):
    """Self correction record returned by the API."""

    correction_id: str
    error_source: str
    error_description: str
    correction_strategy: str
    corrected_output: str
    confidence_score: int
    correction_status: str
    status: str
    progress_percentage: int
    created_at: str
    updated_at: str

    @classmethod
    def from_record(
        cls,
        record: SelfCorrectionRecord,
    ) -> "SelfCorrectionRecordResponse":
        """Build an API response from a stored self correction record."""
        return cls(
            correction_id=record.correction_id,
            error_source=record.error_source,
            error_description=record.error_description,
            correction_strategy=record.correction_strategy,
            corrected_output=record.corrected_output,
            confidence_score=record.confidence_score,
            correction_status=record.correction_status,
            status=record.status,
            progress_percentage=record.progress_percentage,
            created_at=record.created_at,
            updated_at=record.updated_at,
        )


class UserSelfCorrectionEngineResponse(BaseModel):
    """All self correction records for one user."""

    user_id: str
    correction_records: list[SelfCorrectionRecordResponse]
