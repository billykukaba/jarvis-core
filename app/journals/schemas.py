"""Pydantic schemas for the Journal Service."""

from pydantic import BaseModel, Field


class JournalEntry(BaseModel):
    """Journal entry data stored for a user."""

    title: str = Field(min_length=1, description="Journal entry title")
    content: str = Field(min_length=1, description="Journal entry content")
    date: str = Field(min_length=1, description="Entry date (YYYY-MM-DD)")


class JournalEntryResponse(BaseModel):
    """Journal entry returned by the API."""

    title: str
    content: str
    date: str

    @classmethod
    def from_entry(cls, entry: JournalEntry) -> "JournalEntryResponse":
        """Build an API response from a stored journal entry."""
        return cls(
            title=entry.title,
            content=entry.content,
            date=entry.date,
        )


class UserJournalEntriesResponse(BaseModel):
    """All journal entries for one user."""

    user_id: str
    entries: list[JournalEntryResponse]
