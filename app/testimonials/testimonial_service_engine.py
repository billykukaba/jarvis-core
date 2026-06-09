"""Testimonials Service engine with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.testimonials.schemas import TestimonialRecord

# In-memory testimonial store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "name": "Jane Smith",
#             "role": "CTO at OpenAI",
#             "message": "Billy is an exceptional engineer.",
#         }
#     ]
# }
testimonials_db: dict[str, list[TestimonialRecord]] = {}


def normalize_name(name: str) -> str:
    """Normalize a name for case-insensitive, whitespace-tolerant lookups."""
    return name.strip().lower()


class TestimonialServiceEngine:
    """Manage user testimonial records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def name_exists(self, user_id: str, name: str) -> bool:
        """Return True if a testimonial with this name already exists."""
        with self._lock:
            return self._find_record_index(
                testimonials_db.get(user_id, []),
                name,
            ) is not None

    def create_record(
        self,
        user_id: str,
        record: TestimonialRecord,
    ) -> TestimonialRecord:
        """Create and store a testimonial record for the given user."""
        with self._lock:
            user_records = testimonials_db.setdefault(user_id, [])
            user_records.append(record)

        return record

    def get_records(self, user_id: str) -> list[TestimonialRecord]:
        """Return all testimonial records for the given user."""
        with self._lock:
            return list(testimonials_db.get(user_id, []))

    def get_record(self, user_id: str, name: str) -> TestimonialRecord | None:
        """Return one testimonial record by name for the given user."""
        with self._lock:
            return self._find_record(user_id, name)

    def update_record(
        self,
        user_id: str,
        name: str,
        record: TestimonialRecord,
    ) -> TestimonialRecord | None:
        """Replace an existing testimonial record with a new version."""
        with self._lock:
            user_records = testimonials_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, name)
            if index is None:
                return None

            user_records[index] = record

        return record

    def delete_record(self, user_id: str, name: str) -> TestimonialRecord | None:
        """Delete and return a testimonial record by name."""
        with self._lock:
            user_records = testimonials_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, name)
            if index is None:
                return None

            return user_records.pop(index)

    def _find_record(self, user_id: str, name: str) -> TestimonialRecord | None:
        """Locate a testimonial record in the user's list by name."""
        user_records = testimonials_db.get(user_id, [])
        index = self._find_record_index(user_records, name)
        if index is None:
            return None
        return user_records[index]

    @staticmethod
    def _find_record_index(
        user_records: list[TestimonialRecord],
        name: str,
    ) -> int | None:
        """Return the list index for a testimonial name, if it exists."""
        normalized_name = normalize_name(name)
        for index, record in enumerate(user_records):
            if normalize_name(record.name) == normalized_name:
                return index
        return None
