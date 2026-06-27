"""Pydantic schemas for the Self Evaluation Engine."""

from pydantic import BaseModel, ConfigDict, Field


class SelfEvaluationRecord(BaseModel):
    """Self-evaluation record stored for a user."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "evaluation_id": "eval_001",
                    "category": "Reasoning",
                    "score": 9,
                    "feedback": "Reasoning quality improved significantly",
                }
            ]
        }
    )

    evaluation_id: str = Field(
        min_length=1,
        description="Unique self-evaluation record identifier",
        examples=["eval_001"],
    )
    category: str = Field(
        min_length=1,
        description="Evaluation category",
        examples=["Reasoning"],
    )
    score: int = Field(
        ge=0,
        le=10,
        description="Self-evaluation score from 0 to 10",
        examples=[9],
    )
    feedback: str = Field(
        min_length=1,
        description="Self-evaluation feedback text",
        examples=["Reasoning quality improved significantly"],
    )


class SelfEvaluationRecordResponse(BaseModel):
    """Self-evaluation record returned by the API."""

    evaluation_id: str
    category: str
    score: int
    feedback: str

    @classmethod
    def from_record(
        cls,
        record: SelfEvaluationRecord,
    ) -> "SelfEvaluationRecordResponse":
        """Build an API response from a stored self-evaluation record."""
        return cls(
            evaluation_id=record.evaluation_id,
            category=record.category,
            score=record.score,
            feedback=record.feedback,
        )


class UserSelfEvaluationEngineResponse(BaseModel):
    """All self-evaluation records for one user."""

    user_id: str
    self_evaluations: list[SelfEvaluationRecordResponse]
