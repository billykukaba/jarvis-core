"""Pydantic schemas for the Cognitive Growth Tracker Engine."""

from pydantic import BaseModel, ConfigDict, Field


class CognitiveGrowthRecord(BaseModel):
    """Cognitive growth record stored for a user."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "growth_id": "growth_001",
                    "cognitive_area": "Reasoning",
                    "previous_score": 40,
                    "current_score": 80,
                    "growth_percentage": 100,
                }
            ]
        }
    )

    growth_id: str = Field(
        min_length=1,
        description="Unique cognitive growth record identifier",
        examples=["growth_001"],
    )
    cognitive_area: str = Field(
        min_length=1,
        description="Cognitive area being tracked",
        examples=["Reasoning"],
    )
    previous_score: int = Field(
        ge=0,
        description="Previous cognitive score",
        examples=[40],
    )
    current_score: int = Field(
        ge=0,
        description="Current cognitive score",
        examples=[80],
    )
    growth_percentage: int = Field(
        ge=0,
        description="Growth percentage between previous and current scores",
        examples=[100],
    )


class CognitiveGrowthRecordResponse(BaseModel):
    """Cognitive growth record returned by the API."""

    growth_id: str
    cognitive_area: str
    previous_score: int
    current_score: int
    growth_percentage: int

    @classmethod
    def from_record(
        cls,
        record: CognitiveGrowthRecord,
    ) -> "CognitiveGrowthRecordResponse":
        """Build an API response from a stored cognitive growth record."""
        return cls(
            growth_id=record.growth_id,
            cognitive_area=record.cognitive_area,
            previous_score=record.previous_score,
            current_score=record.current_score,
            growth_percentage=record.growth_percentage,
        )


class UserCognitiveGrowthTrackerResponse(BaseModel):
    """All cognitive growth records for one user."""

    user_id: str
    cognitive_growth_records: list[CognitiveGrowthRecordResponse]
