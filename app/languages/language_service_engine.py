"""Languages Service engine with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.languages.schemas import Language

# In-memory language store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "language": "English",
#             "level": "Fluent",
#         }
#     ]
# }
languages_db: dict[str, list[Language]] = {}


class LanguageServiceEngine:
    """Manage user language records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def language_exists(self, user_id: str, language: str) -> bool:
        """Return True if a record for this language already exists."""
        with self._lock:
            return self._find_language_index(
                languages_db.get(user_id, []),
                language,
            ) is not None

    def create_language(self, user_id: str, language: Language) -> Language:
        """Create and store a language record for the given user."""
        with self._lock:
            user_languages = languages_db.setdefault(user_id, [])
            user_languages.append(language)

        return language

    def get_languages(self, user_id: str) -> list[Language]:
        """Return all language records for the given user."""
        with self._lock:
            return list(languages_db.get(user_id, []))

    def get_language(self, user_id: str, language: str) -> Language | None:
        """Return one language record by language name for the given user."""
        with self._lock:
            return self._find_language(user_id, language)

    def update_language(
        self,
        user_id: str,
        language: str,
        updated: Language,
    ) -> Language | None:
        """Replace an existing language record with a new version."""
        with self._lock:
            user_languages = languages_db.get(user_id)
            if user_languages is None:
                return None

            index = self._find_language_index(user_languages, language)
            if index is None:
                return None

            user_languages[index] = updated

        return updated

    def delete_language(self, user_id: str, language: str) -> Language | None:
        """Delete and return a language record by language name."""
        with self._lock:
            user_languages = languages_db.get(user_id)
            if user_languages is None:
                return None

            index = self._find_language_index(user_languages, language)
            if index is None:
                return None

            return user_languages.pop(index)

    def _find_language(self, user_id: str, language: str) -> Language | None:
        """Locate a language record in the user's list by language name."""
        user_languages = languages_db.get(user_id, [])
        index = self._find_language_index(user_languages, language)
        if index is None:
            return None
        return user_languages[index]

    @staticmethod
    def _find_language_index(
        user_languages: list[Language],
        language: str,
    ) -> int | None:
        """Return the list index for a language name, if it exists."""
        normalized_language = language.lower()
        for index, record in enumerate(user_languages):
            if record.language.lower() == normalized_language:
                return index
        return None
