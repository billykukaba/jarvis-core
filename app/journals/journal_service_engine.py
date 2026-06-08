"""Journal Service engine with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.journals.schemas import JournalEntry

# In-memory journal store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "title": "MIT Progress",
#             "content": "Today I studied Flutter and AI.",
#             "date": "2026-06-07",
#         }
#     ]
# }
journals_db: dict[str, list[JournalEntry]] = {}


class JournalServiceEngine:
    """Manage user journal entries stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def create_entry(self, user_id: str, entry: JournalEntry) -> JournalEntry:
        """Create and store a journal entry for the given user."""
        with self._lock:
            user_entries = journals_db.setdefault(user_id, [])
            user_entries.append(entry)

        return entry

    def get_entries(self, user_id: str) -> list[JournalEntry]:
        """Return all journal entries for the given user."""
        with self._lock:
            return list(journals_db.get(user_id, []))

    def get_entry(self, user_id: str, title: str) -> JournalEntry | None:
        """Return one journal entry by title for the given user."""
        with self._lock:
            return self._find_entry(user_id, title)

    def update_entry(
        self,
        user_id: str,
        title: str,
        entry: JournalEntry,
    ) -> JournalEntry | None:
        """Replace an existing journal entry with a new version."""
        with self._lock:
            user_entries = journals_db.get(user_id)
            if user_entries is None:
                return None

            index = self._find_entry_index(user_entries, title)
            if index is None:
                return None

            user_entries[index] = entry

        return entry

    def delete_entry(self, user_id: str, title: str) -> JournalEntry | None:
        """Delete and return a journal entry by title."""
        with self._lock:
            user_entries = journals_db.get(user_id)
            if user_entries is None:
                return None

            index = self._find_entry_index(user_entries, title)
            if index is None:
                return None

            return user_entries.pop(index)

    def _find_entry(self, user_id: str, title: str) -> JournalEntry | None:
        """Locate a journal entry in the user's list by title."""
        user_entries = journals_db.get(user_id, [])
        index = self._find_entry_index(user_entries, title)
        if index is None:
            return None
        return user_entries[index]

    @staticmethod
    def _find_entry_index(user_entries: list[JournalEntry], title: str) -> int | None:
        """Return the list index for a journal title, if it exists."""
        normalized_title = title.lower()
        for index, entry in enumerate(user_entries):
            if entry.title.lower() == normalized_title:
                return index
        return None
