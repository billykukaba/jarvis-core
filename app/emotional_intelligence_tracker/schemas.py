"""Pydantic schemas for the Emotional Intelligence Tracker Engine (Module 63)."""

from pydantic import BaseModel, ConfigDict, Field


class EmotionalIntelligenceRecord(BaseModel):
    """Emotional intelligence record stored for a user."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "eq_id": "eq_001",
                    "self_awareness": 80,
                    "self_regulation": 75,
                    "empathy": 90,
                    "social_skills": 85,
                    "motivation": 88,
                    "overall_eq": 84,
                }
            ]
        }
    )

    eq_id: str = Field(
        min_length=1,
        description="Unique emotional intelligence record identifier",
        examples=["eq_001"],
    )
    self_awareness: int = Field(
        ge=0,
        le=100,
        description="Self-awareness score",
        examples=[80],
    )
    self_regulation: int = Field(
        ge=0,
        le=100,
        description="Self-regulation score",
        examples=[75],
    )
    empathy: int = Field(
        ge=0,
        le=100,
        description="Empathy score",
        examples=[90],
    )
    social_skills: int = Field(
        ge=0,
        le=100,
        description="Social skills score",
        examples=[85],
    )
    motivation: int = Field(
        ge=0,
        le=100,
        description="Motivation score",
        examples=[88],
    )
    overall_eq: int = Field(
        ge=0,
        le=100,
        description="Overall emotional intelligence score",
        examples=[84],
    )


class EmotionalIntelligenceRecordResponse(BaseModel):
    """Emotional intelligence record returned by the API."""

    eq_id: str
    self_awareness: int
    self_regulation: int
    empathy: int
    social_skills: int
    motivation: int
    overall_eq: int

    @classmethod
    def from_record(
        cls,
        record: EmotionalIntelligenceRecord,
    ) -> "EmotionalIntelligenceRecordResponse":
        """Build an API response from a stored EQ record."""
        return cls(
            eq_id=record.eq_id,
            self_awareness=record.self_awareness,
            self_regulation=record.self_regulation,
            empathy=record.empathy,
            social_skills=record.social_skills,
            motivation=record.motivation,
            overall_eq=record.overall_eq,
        )


class UserEmotionalIntelligenceTrackerResponse(BaseModel):
    """All emotional intelligence records for one user."""

    user_id: str
    eq_records: list[EmotionalIntelligenceRecordResponse]
