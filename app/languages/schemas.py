"""Pydantic schemas for the Languages Service."""

from pydantic import BaseModel, Field


class Language(BaseModel):
    """Language proficiency record stored for a user."""

    language: str = Field(min_length=1, description="Language name")
    level: str = Field(min_length=1, description="Proficiency level (e.g. Beginner, Fluent)")


class LanguageResponse(BaseModel):
    """Language record returned by the API."""

    language: str
    level: str

    @classmethod
    def from_language(cls, language: Language) -> "LanguageResponse":
        """Build an API response from a stored language record."""
        return cls(
            language=language.language,
            level=language.level,
        )


class UserLanguagesResponse(BaseModel):
    """All language records for one user."""

    user_id: str
    languages: list[LanguageResponse]
