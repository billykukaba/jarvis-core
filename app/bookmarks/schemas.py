"""Pydantic schemas for the Bookmark Service."""

from pydantic import BaseModel, Field, HttpUrl


class Bookmark(BaseModel):
    """Bookmark data stored for a user."""

    title: str = Field(min_length=1, description="Bookmark title")
    url: HttpUrl = Field(description="Bookmark URL")
    category: str = Field(min_length=1, description="Bookmark category")


class BookmarkResponse(BaseModel):
    """Bookmark returned by the API."""

    title: str
    url: str
    category: str

    @classmethod
    def from_bookmark(cls, bookmark: Bookmark) -> "BookmarkResponse":
        """Build an API response from a stored bookmark."""
        return cls(
            title=bookmark.title,
            url=str(bookmark.url),
            category=bookmark.category,
        )


class UserBookmarksResponse(BaseModel):
    """All bookmarks for one user."""

    user_id: str
    bookmarks: list[BookmarkResponse]
