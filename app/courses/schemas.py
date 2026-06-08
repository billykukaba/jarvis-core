"""Pydantic schemas for the Courses Service (Module 58)."""

from pydantic import BaseModel, ConfigDict, Field


class CourseRecord(BaseModel):
    """Online course record stored for a user."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "title": "Advanced Deep Learning",
                    "platform": "Coursera",
                    "year": 2032,
                }
            ]
        }
    )

    title: str = Field(
        min_length=1,
        description="Course title",
        examples=["Advanced Deep Learning"],
    )
    platform: str = Field(
        min_length=1,
        description="Learning platform or provider",
        examples=["Coursera"],
    )
    year: int = Field(
        ge=1900,
        description="Completion or enrollment year (>= 1900)",
        examples=[2032],
    )


class CourseRecordResponse(BaseModel):
    """Course record returned by the API."""

    title: str
    platform: str
    year: int

    @classmethod
    def from_record(cls, record: CourseRecord) -> "CourseRecordResponse":
        """Build an API response from a stored course record."""
        return cls(
            title=record.title,
            platform=record.platform,
            year=record.year,
        )


class UserCoursesResponse(BaseModel):
    """All course records for one user."""

    user_id: str
    courses: list[CourseRecordResponse]
