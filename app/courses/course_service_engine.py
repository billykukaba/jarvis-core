"""Courses Service engine with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.courses.schemas import CourseRecord

# In-memory course store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "title": "Advanced Deep Learning",
#             "platform": "Coursera",
#             "year": 2032,
#         }
#     ]
# }
courses_db: dict[str, list[CourseRecord]] = {}


def normalize_title(title: str) -> str:
    """Normalize a title for case-insensitive, whitespace-tolerant lookups."""
    return title.strip().lower()


class CourseServiceEngine:
    """Manage user course records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def title_exists(self, user_id: str, title: str) -> bool:
        """Return True if a course with this title already exists."""
        with self._lock:
            return self._find_record_index(
                courses_db.get(user_id, []),
                title,
            ) is not None

    def create_record(self, user_id: str, record: CourseRecord) -> CourseRecord:
        """Create and store a course record for the given user."""
        with self._lock:
            user_records = courses_db.setdefault(user_id, [])
            user_records.append(record)

        return record

    def get_records(self, user_id: str) -> list[CourseRecord]:
        """Return all course records for the given user."""
        with self._lock:
            return list(courses_db.get(user_id, []))

    def get_record(self, user_id: str, title: str) -> CourseRecord | None:
        """Return one course record by title for the given user."""
        with self._lock:
            return self._find_record(user_id, title)

    def update_record(
        self,
        user_id: str,
        title: str,
        record: CourseRecord,
    ) -> CourseRecord | None:
        """Replace an existing course record with a new version."""
        with self._lock:
            user_records = courses_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, title)
            if index is None:
                return None

            user_records[index] = record

        return record

    def delete_record(self, user_id: str, title: str) -> CourseRecord | None:
        """Delete and return a course record by title."""
        with self._lock:
            user_records = courses_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, title)
            if index is None:
                return None

            return user_records.pop(index)

    def _find_record(self, user_id: str, title: str) -> CourseRecord | None:
        """Locate a course record in the user's list by title."""
        user_records = courses_db.get(user_id, [])
        index = self._find_record_index(user_records, title)
        if index is None:
            return None
        return user_records[index]

    @staticmethod
    def _find_record_index(
        user_records: list[CourseRecord],
        title: str,
    ) -> int | None:
        """Return the list index for a course title, if it exists."""
        normalized_title = normalize_title(title)
        for index, record in enumerate(user_records):
            if normalize_title(record.title) == normalized_title:
                return index
        return None
