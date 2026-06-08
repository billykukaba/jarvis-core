"""Bookmark engine with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.bookmarks.schemas import Bookmark

# In-memory bookmark store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "title": "MIT AI Course",
#             "url": "https://...",
#             "category": "Education",
#         }
#     ]
# }
bookmarks_db: dict[str, list[Bookmark]] = {}


class BookmarkEngine:
    """Manage user bookmarks stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def create_bookmark(self, user_id: str, bookmark: Bookmark) -> Bookmark:
        """Create and store a bookmark for the given user."""
        with self._lock:
            user_bookmarks = bookmarks_db.setdefault(user_id, [])
            user_bookmarks.append(bookmark)

        return bookmark

    def get_bookmarks(self, user_id: str) -> list[Bookmark]:
        """Return all bookmarks for the given user."""
        with self._lock:
            return list(bookmarks_db.get(user_id, []))

    def get_bookmark(self, user_id: str, title: str) -> Bookmark | None:
        """Return one bookmark by title for the given user."""
        with self._lock:
            return self._find_bookmark(user_id, title)

    def update_bookmark(
        self,
        user_id: str,
        title: str,
        bookmark: Bookmark,
    ) -> Bookmark | None:
        """Replace an existing bookmark with a new version."""
        with self._lock:
            user_bookmarks = bookmarks_db.get(user_id)
            if user_bookmarks is None:
                return None

            index = self._find_bookmark_index(user_bookmarks, title)
            if index is None:
                return None

            user_bookmarks[index] = bookmark

        return bookmark

    def delete_bookmark(self, user_id: str, title: str) -> Bookmark | None:
        """Delete and return a bookmark by title."""
        with self._lock:
            user_bookmarks = bookmarks_db.get(user_id)
            if user_bookmarks is None:
                return None

            index = self._find_bookmark_index(user_bookmarks, title)
            if index is None:
                return None

            return user_bookmarks.pop(index)

    def _find_bookmark(self, user_id: str, title: str) -> Bookmark | None:
        """Locate a bookmark in the user's list by title."""
        user_bookmarks = bookmarks_db.get(user_id, [])
        index = self._find_bookmark_index(user_bookmarks, title)
        if index is None:
            return None
        return user_bookmarks[index]

    @staticmethod
    def _find_bookmark_index(user_bookmarks: list[Bookmark], title: str) -> int | None:
        """Return the list index for a bookmark title, if it exists."""
        normalized_title = title.lower()
        for index, bookmark in enumerate(user_bookmarks):
            if bookmark.title.lower() == normalized_title:
                return index
        return None
