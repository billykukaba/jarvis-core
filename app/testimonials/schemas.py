"""Pydantic schemas for the Testimonials Service (Module 61)."""

from pydantic import BaseModel, ConfigDict, Field


class TestimonialRecord(BaseModel):
    """Testimonial record stored for a user."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "name": "Jane Smith",
                    "role": "CTO at OpenAI",
                    "message": "Billy is an exceptional engineer.",
                }
            ]
        }
    )

    name: str = Field(
        min_length=1,
        description="Name of the person giving the testimonial",
        examples=["Jane Smith"],
    )
    role: str = Field(
        min_length=1,
        description="Professional role or title of the person",
        examples=["CTO at OpenAI"],
    )
    message: str = Field(
        min_length=1,
        description="Testimonial message or quote",
        examples=["Billy is an exceptional engineer."],
    )


class TestimonialRecordResponse(BaseModel):
    """Testimonial record returned by the API."""

    name: str
    role: str
    message: str

    @classmethod
    def from_record(cls, record: TestimonialRecord) -> "TestimonialRecordResponse":
        """Build an API response from a stored testimonial record."""
        return cls(
            name=record.name,
            role=record.role,
            message=record.message,
        )


class UserTestimonialsResponse(BaseModel):
    """All testimonial records for one user."""

    user_id: str
    testimonials: list[TestimonialRecordResponse]
