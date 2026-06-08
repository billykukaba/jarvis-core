"""Pydantic schemas for the Testimonials Service (Module 61)."""

from pydantic import BaseModel, ConfigDict, Field


class TestimonialRecord(BaseModel):
    """Testimonial record stored for a user."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "name": "Dr. Jane Smith",
                    "role": "Professor of AI",
                    "message": "An exceptional student with deep technical skills.",
                }
            ]
        }
    )

    name: str = Field(
        min_length=1,
        description="Person providing the testimonial",
        examples=["Dr. Jane Smith"],
    )
    role: str = Field(
        min_length=1,
        description="Role or relationship of the person",
        examples=["Professor of AI"],
    )
    message: str = Field(
        min_length=1,
        description="Testimonial message or endorsement",
        examples=["An exceptional student with deep technical skills."],
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
