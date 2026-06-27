"""Learning Planner Engine with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.learning_planner.schemas import LearningPlan

# In-memory learning planner store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "plan_id": "plan_001",
#             "subject": "Python",
#             "goal": "Master FastAPI development",
#             "progress": 0,
#         }
#     ]
# }
learning_planner_store: dict[str, list[LearningPlan]] = {}


def normalize_plan_id(plan_id: str) -> str:
    """Normalize a plan ID for case-insensitive, whitespace-tolerant lookups."""
    return plan_id.strip().lower()


class LearningPlannerEngine:
    """Manage user learning plan records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def plan_id_exists(self, user_id: str, plan_id: str) -> bool:
        """Return True if a record for this plan ID already exists."""
        with self._lock:
            return self._find_record_index(
                learning_planner_store.get(user_id, []),
                plan_id,
            ) is not None

    def create_record(self, user_id: str, record: LearningPlan) -> LearningPlan:
        """Create and store a learning plan for the given user."""
        with self._lock:
            user_records = learning_planner_store.setdefault(user_id, [])
            user_records.append(record)

        return record

    def get_records(self, user_id: str) -> list[LearningPlan]:
        """Return all learning plans for the given user."""
        with self._lock:
            return list(learning_planner_store.get(user_id, []))

    def get_record(self, user_id: str, plan_id: str) -> LearningPlan | None:
        """Return one learning plan by ID for the given user."""
        with self._lock:
            return self._find_record(user_id, plan_id)

    def update_record(
        self,
        user_id: str,
        plan_id: str,
        record: LearningPlan,
    ) -> LearningPlan | None:
        """Replace an existing learning plan with a new version."""
        with self._lock:
            user_records = learning_planner_store.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, plan_id)
            if index is None:
                return None

            user_records[index] = record

        return record

    def delete_record(self, user_id: str, plan_id: str) -> LearningPlan | None:
        """Delete and return a learning plan by ID."""
        with self._lock:
            user_records = learning_planner_store.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, plan_id)
            if index is None:
                return None

            return user_records.pop(index)

    def _find_record(self, user_id: str, plan_id: str) -> LearningPlan | None:
        """Locate a learning plan in the user's list by ID."""
        user_records = learning_planner_store.get(user_id, [])
        index = self._find_record_index(user_records, plan_id)
        if index is None:
            return None
        return user_records[index]

    @staticmethod
    def _find_record_index(
        user_records: list[LearningPlan],
        plan_id: str,
    ) -> int | None:
        """Return the list index for a plan ID, if it exists."""
        normalized_id = normalize_plan_id(plan_id)
        for index, record in enumerate(user_records):
            if normalize_plan_id(record.plan_id) == normalized_id:
                return index
        return None
