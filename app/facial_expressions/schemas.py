"""Pydantic schemas for the Facial Expression Service (Module 63)."""

from pydantic import BaseModel, ConfigDict, Field


class FacialExpressionRecord(BaseModel):
    """Facial expression record stored for a user."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "expression": "Happy",
                    "avatar_state": "Smiling",
                }
            ]
        }
    )

    expression: str = Field(
        min_length=1,
        description="Facial expression name",
        examples=["Happy"],
    )
    avatar_state: str = Field(
        min_length=1,
        description="Avatar visual state for the expression",
        examples=["Smiling"],
    )


class FacialExpressionRecordResponse(BaseModel):
    """Facial expression record returned by the API."""

    expression: str
    avatar_state: str

    @classmethod
    def from_record(
        cls,
        record: FacialExpressionRecord,
    ) -> "FacialExpressionRecordResponse":
        """Build an API response from a stored facial expression record."""
        return cls(
            expression=record.expression,
            avatar_state=record.avatar_state,
        )


class UserFacialExpressionsResponse(BaseModel):
    """All facial expression records for one user."""

    user_id: str
    facial_expressions: list[FacialExpressionRecordResponse]
