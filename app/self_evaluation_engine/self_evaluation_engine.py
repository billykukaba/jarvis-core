"""Self Evaluation Engine with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.self_evaluation_engine.schemas import SelfEvaluationRecord

# In-memory self-evaluation store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "evaluation_id": "eval_001",
#             "category": "Reasoning",
#             "score": 9,
#             "feedback": "Reasoning quality improved significantly",
#         }
#     ]
# }
self_evaluation_db: dict[str, list[SelfEvaluationRecord]] = {}


def normalize_evaluation_id(evaluation_id: str) -> str:
    """Normalize an evaluation ID for case-insensitive, whitespace-tolerant lookups."""
    return evaluation_id.strip().lower()


class SelfEvaluationEngine:
    """Manage user self-evaluation records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def evaluation_id_exists(self, user_id: str, evaluation_id: str) -> bool:
        """Return True if a record for this evaluation ID already exists."""
        with self._lock:
            return self._find_record_index(
                self_evaluation_db.get(user_id, []),
                evaluation_id,
            ) is not None

    def create_record(
        self,
        user_id: str,
        record: SelfEvaluationRecord,
    ) -> SelfEvaluationRecord:
        """Create and store a self-evaluation record for the given user."""
        with self._lock:
            user_records = self_evaluation_db.setdefault(user_id, [])
            user_records.append(record)

        return record

    def get_records(self, user_id: str) -> list[SelfEvaluationRecord]:
        """Return all self-evaluation records for the given user."""
        with self._lock:
            return list(self_evaluation_db.get(user_id, []))

    def get_record(
        self,
        user_id: str,
        evaluation_id: str,
    ) -> SelfEvaluationRecord | None:
        """Return one self-evaluation record by ID for the given user."""
        with self._lock:
            return self._find_record(user_id, evaluation_id)

    def update_record(
        self,
        user_id: str,
        evaluation_id: str,
        record: SelfEvaluationRecord,
    ) -> SelfEvaluationRecord | None:
        """Replace an existing self-evaluation record with a new version."""
        with self._lock:
            user_records = self_evaluation_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, evaluation_id)
            if index is None:
                return None

            user_records[index] = record

        return record

    def delete_record(
        self,
        user_id: str,
        evaluation_id: str,
    ) -> SelfEvaluationRecord | None:
        """Delete and return a self-evaluation record by ID."""
        with self._lock:
            user_records = self_evaluation_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, evaluation_id)
            if index is None:
                return None

            return user_records.pop(index)

    def _find_record(
        self,
        user_id: str,
        evaluation_id: str,
    ) -> SelfEvaluationRecord | None:
        """Locate a self-evaluation record in the user's list by ID."""
        user_records = self_evaluation_db.get(user_id, [])
        index = self._find_record_index(user_records, evaluation_id)
        if index is None:
            return None
        return user_records[index]

    @staticmethod
    def _find_record_index(
        user_records: list[SelfEvaluationRecord],
        evaluation_id: str,
    ) -> int | None:
        """Return the list index for an evaluation ID, if it exists."""
        normalized_id = normalize_evaluation_id(evaluation_id)
        for index, record in enumerate(user_records):
            if normalize_evaluation_id(record.evaluation_id) == normalized_id:
                return index
        return None
