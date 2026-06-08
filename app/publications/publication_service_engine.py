"""Publications Service engine with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.publications.schemas import Publication

# In-memory publication store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "title": "AI for Social Networks",
#             "publisher": "MIT Press",
#             "year": 2032,
#         }
#     ]
# }
publications_db: dict[str, list[Publication]] = {}


class PublicationServiceEngine:
    """Manage user publication records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def title_exists(self, user_id: str, title: str) -> bool:
        """Return True if a publication with this title already exists."""
        with self._lock:
            return self._find_publication_index(
                publications_db.get(user_id, []),
                title,
            ) is not None

    def create_publication(
        self,
        user_id: str,
        publication: Publication,
    ) -> Publication:
        """Create and store a publication record for the given user."""
        with self._lock:
            user_publications = publications_db.setdefault(user_id, [])
            user_publications.append(publication)

        return publication

    def get_publications(self, user_id: str) -> list[Publication]:
        """Return all publication records for the given user."""
        with self._lock:
            return list(publications_db.get(user_id, []))

    def get_publication(self, user_id: str, title: str) -> Publication | None:
        """Return one publication record by title for the given user."""
        with self._lock:
            return self._find_publication(user_id, title)

    def update_publication(
        self,
        user_id: str,
        title: str,
        publication: Publication,
    ) -> Publication | None:
        """Replace an existing publication record with a new version."""
        with self._lock:
            user_publications = publications_db.get(user_id)
            if user_publications is None:
                return None

            index = self._find_publication_index(user_publications, title)
            if index is None:
                return None

            user_publications[index] = publication

        return publication

    def delete_publication(self, user_id: str, title: str) -> Publication | None:
        """Delete and return a publication record by title."""
        with self._lock:
            user_publications = publications_db.get(user_id)
            if user_publications is None:
                return None

            index = self._find_publication_index(user_publications, title)
            if index is None:
                return None

            return user_publications.pop(index)

    def _find_publication(self, user_id: str, title: str) -> Publication | None:
        """Locate a publication record in the user's list by title."""
        user_publications = publications_db.get(user_id, [])
        index = self._find_publication_index(user_publications, title)
        if index is None:
            return None
        return user_publications[index]

    @staticmethod
    def _find_publication_index(
        user_publications: list[Publication],
        title: str,
    ) -> int | None:
        """Return the list index for a publication title, if it exists."""
        normalized_title = title.lower()
        for index, publication in enumerate(user_publications):
            if publication.title.lower() == normalized_title:
                return index
        return None
