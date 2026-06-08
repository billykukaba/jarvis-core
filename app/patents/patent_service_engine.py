"""Patents Service engine with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.patents.schemas import Patent

# In-memory patent store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "title": "AI Recommendation Engine",
#             "patent_number": "US123456",
#             "year": 2034,
#         }
#     ]
# }
patents_db: dict[str, list[Patent]] = {}


class PatentServiceEngine:
    """Manage user patent records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def title_exists(self, user_id: str, title: str) -> bool:
        """Return True if a patent with this title already exists."""
        with self._lock:
            return self._find_patent_index(
                patents_db.get(user_id, []),
                title,
            ) is not None

    def create_patent(self, user_id: str, patent: Patent) -> Patent:
        """Create and store a patent record for the given user."""
        with self._lock:
            user_patents = patents_db.setdefault(user_id, [])
            user_patents.append(patent)

        return patent

    def get_patents(self, user_id: str) -> list[Patent]:
        """Return all patent records for the given user."""
        with self._lock:
            return list(patents_db.get(user_id, []))

    def get_patent(self, user_id: str, title: str) -> Patent | None:
        """Return one patent record by title for the given user."""
        with self._lock:
            return self._find_patent(user_id, title)

    def update_patent(
        self,
        user_id: str,
        title: str,
        patent: Patent,
    ) -> Patent | None:
        """Replace an existing patent record with a new version."""
        with self._lock:
            user_patents = patents_db.get(user_id)
            if user_patents is None:
                return None

            index = self._find_patent_index(user_patents, title)
            if index is None:
                return None

            user_patents[index] = patent

        return patent

    def delete_patent(self, user_id: str, title: str) -> Patent | None:
        """Delete and return a patent record by title."""
        with self._lock:
            user_patents = patents_db.get(user_id)
            if user_patents is None:
                return None

            index = self._find_patent_index(user_patents, title)
            if index is None:
                return None

            return user_patents.pop(index)

    def _find_patent(self, user_id: str, title: str) -> Patent | None:
        """Locate a patent record in the user's list by title."""
        user_patents = patents_db.get(user_id, [])
        index = self._find_patent_index(user_patents, title)
        if index is None:
            return None
        return user_patents[index]

    @staticmethod
    def _find_patent_index(
        user_patents: list[Patent],
        title: str,
    ) -> int | None:
        """Return the list index for a patent title, if it exists."""
        normalized_title = title.lower()
        for index, patent in enumerate(user_patents):
            if patent.title.lower() == normalized_title:
                return index
        return None
