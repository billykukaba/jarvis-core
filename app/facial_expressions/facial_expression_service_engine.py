"""Facial Expression Service engine with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.facial_expressions.schemas import FacialExpressionRecord

# In-memory facial expression store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "expression": "Happy",
#             "avatar_state": "Smiling",
#         }
#     ]
# }
facial_expressions_db: dict[str, list[FacialExpressionRecord]] = {}


def normalize_expression(expression: str) -> str:
    """Normalize an expression for case-insensitive, whitespace-tolerant lookups."""
    return expression.strip().lower()


class FacialExpressionServiceEngine:
    """Manage user facial expression records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def expression_exists(self, user_id: str, expression: str) -> bool:
        """Return True if a record for this expression already exists."""
        with self._lock:
            return self._find_record_index(
                facial_expressions_db.get(user_id, []),
                expression,
            ) is not None

    def create_record(
        self,
        user_id: str,
        record: FacialExpressionRecord,
    ) -> FacialExpressionRecord:
        """Create and store a facial expression record for the given user."""
        with self._lock:
            user_records = facial_expressions_db.setdefault(user_id, [])
            user_records.append(record)

        return record

    def get_records(self, user_id: str) -> list[FacialExpressionRecord]:
        """Return all facial expression records for the given user."""
        with self._lock:
            return list(facial_expressions_db.get(user_id, []))

    def get_record(
        self,
        user_id: str,
        expression: str,
    ) -> FacialExpressionRecord | None:
        """Return one facial expression record by name for the given user."""
        with self._lock:
            return self._find_record(user_id, expression)

    def update_record(
        self,
        user_id: str,
        expression: str,
        record: FacialExpressionRecord,
    ) -> FacialExpressionRecord | None:
        """Replace an existing facial expression record with a new version."""
        with self._lock:
            user_records = facial_expressions_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, expression)
            if index is None:
                return None

            user_records[index] = record

        return record

    def delete_record(
        self,
        user_id: str,
        expression: str,
    ) -> FacialExpressionRecord | None:
        """Delete and return a facial expression record by name."""
        with self._lock:
            user_records = facial_expressions_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, expression)
            if index is None:
                return None

            return user_records.pop(index)

    def _find_record(
        self,
        user_id: str,
        expression: str,
    ) -> FacialExpressionRecord | None:
        """Locate a facial expression record in the user's list by name."""
        user_records = facial_expressions_db.get(user_id, [])
        index = self._find_record_index(user_records, expression)
        if index is None:
            return None
        return user_records[index]

    @staticmethod
    def _find_record_index(
        user_records: list[FacialExpressionRecord],
        expression: str,
    ) -> int | None:
        """Return the list index for an expression name, if it exists."""
        normalized_expression = normalize_expression(expression)
        for index, record in enumerate(user_records):
            if normalize_expression(record.expression) == normalized_expression:
                return index
        return None
