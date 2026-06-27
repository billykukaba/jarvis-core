"""Pydantic schemas for the Knowledge Gap Detector Engine (Module 59)."""

from pydantic import BaseModel, ConfigDict, Field


class KnowledgeGap(BaseModel):
    """Knowledge gap record stored for a user."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "gap_id": "gap_001",
                    "topic": "FastAPI Middleware",
                    "severity": 8,
                    "recommendation": "Study middleware lifecycle and custom middleware patterns",
                }
            ]
        }
    )

    gap_id: str = Field(
        min_length=1,
        description="Unique knowledge gap identifier",
        examples=["gap_001"],
    )
    topic: str = Field(
        min_length=1,
        description="Knowledge gap topic",
        examples=["FastAPI Middleware"],
    )
    severity: int = Field(
        ge=0,
        le=10,
        description="Gap severity level from 0 to 10",
        examples=[8],
    )
    recommendation: str = Field(
        min_length=1,
        description="Recommended action to address the gap",
        examples=["Study middleware lifecycle and custom middleware patterns"],
    )


class KnowledgeGapResponse(BaseModel):
    """Knowledge gap record returned by the API."""

    gap_id: str
    topic: str
    severity: int
    recommendation: str

    @classmethod
    def from_gap(cls, gap: KnowledgeGap) -> "KnowledgeGapResponse":
        """Build an API response from a stored knowledge gap record."""
        return cls(
            gap_id=gap.gap_id,
            topic=gap.topic,
            severity=gap.severity,
            recommendation=gap.recommendation,
        )


class UserKnowledgeGapDetectorResponse(BaseModel):
    """All knowledge gap records for one user."""

    user_id: str
    knowledge_gaps: list[KnowledgeGapResponse]
