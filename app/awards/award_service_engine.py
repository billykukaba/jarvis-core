"""Awards Service engine with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.awards.schemas import Award

# In-memory award store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "title": "Best AI Project",
#             "issuer": "MIT",
#             "year": 2033,
#         }
#     ]
# }
awards_db: dict[str, list[Award]] = {}


def normalize_title(title: str) -> str:
    """Normalize a title for case-insensitive, whitespace-tolerant lookups."""
    return title.strip().lower()


class AwardServiceEngine:
    """Manage user award records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def title_exists(self, user_id: str, title: str) -> bool:
        """Return True if another award already uses this title."""
        with self._lock:
            return self._find_award_index(
                awards_db.get(user_id, []),
                title,
            ) is not None

    def create_award(self, user_id: str, award: Award) -> Award:
        """Create and store an award record for the given user."""
        with self._lock:
            user_awards = awards_db.setdefault(user_id, [])
            user_awards.append(award)

        return award

    def get_awards(self, user_id: str) -> list[Award]:
        """Return all award records for the given user."""
        with self._lock:
            return list(awards_db.get(user_id, []))

    def get_award(self, user_id: str, title: str) -> Award | None:
        """Return one award record by title for the given user."""
        with self._lock:
            return self._find_award(user_id, title)

    def update_award(
        self,
        user_id: str,
        title: str,
        award: Award,
    ) -> Award | None:
        """Replace an existing award record with a new version."""
        with self._lock:
            user_awards = awards_db.get(user_id)
            if user_awards is None:
                return None

            # Locate the record using the path title, not the request body title.
            index = self._find_award_index(user_awards, title)
            if index is None:
                return None

            user_awards[index] = award

        return award

    def delete_award(self, user_id: str, title: str) -> Award | None:
        """Delete and return an award record by title."""
        with self._lock:
            user_awards = awards_db.get(user_id)
            if user_awards is None:
                return None

            index = self._find_award_index(user_awards, title)
            if index is None:
                return None

            return user_awards.pop(index)

    def _find_award(self, user_id: str, title: str) -> Award | None:
        """Locate an award record in the user's list by title."""
        user_awards = awards_db.get(user_id, [])
        index = self._find_award_index(user_awards, title)
        if index is None:
            return None
        return user_awards[index]

    @staticmethod
    def _find_award_index(
        user_awards: list[Award],
        title: str,
    ) -> int | None:
        """Return the list index for an award title, if it exists."""
        # Compare normalized titles so lookups work with different casing
        # and accidental leading/trailing spaces in the path parameter.
        normalized_title = normalize_title(title)
        for index, award in enumerate(user_awards):
            if normalize_title(award.title) == normalized_title:
                return index
        return None
