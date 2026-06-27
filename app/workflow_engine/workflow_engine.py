"""Workflow Engine with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.workflow_engine.schemas import WorkflowRecord

# In-memory workflow store keyed by user_id, then workflow_id.
# Example:
# {
#     "billy": {
#         "wf_001": {
#             "workflow_id": "wf_001",
#             "workflow_name": "Onboarding Pipeline",
#             "description": "Standard new-hire onboarding workflow",
#             "steps": ["Create account", "Assign mentor", "Complete training"],
#             "status": "in_progress",
#             "progress_percentage": 33.3,
#             "created_at": "2026-06-04T09:00:00",
#             "updated_at": "2026-06-04T10:30:00",
#         }
#     }
# }
workflow_engine_db: dict[str, dict[str, WorkflowRecord]] = {}


def normalize_workflow_id(workflow_id: str) -> str:
    """Normalize a workflow ID for case-insensitive, whitespace-tolerant lookups."""
    return workflow_id.strip().lower()


class WorkflowEngine:
    """Manage user workflow records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def workflow_id_exists(self, user_id: str, workflow_id: str) -> bool:
        """Return True if a record for this workflow ID already exists."""
        with self._lock:
            user_records = workflow_engine_db.get(user_id, {})
            return normalize_workflow_id(workflow_id) in user_records

    def create_record(self, user_id: str, record: WorkflowRecord) -> WorkflowRecord:
        """Create and store a workflow record for the given user."""
        with self._lock:
            user_records = workflow_engine_db.setdefault(user_id, {})
            user_records[normalize_workflow_id(record.workflow_id)] = record

        return record

    def get_records(self, user_id: str) -> list[WorkflowRecord]:
        """Return all workflow records for the given user."""
        with self._lock:
            user_records = workflow_engine_db.get(user_id, {})
            return list(user_records.values())

    def get_record(self, user_id: str, workflow_id: str) -> WorkflowRecord | None:
        """Return one workflow record by ID for the given user."""
        with self._lock:
            user_records = workflow_engine_db.get(user_id, {})
            return user_records.get(normalize_workflow_id(workflow_id))

    def update_record(
        self,
        user_id: str,
        workflow_id: str,
        record: WorkflowRecord,
    ) -> WorkflowRecord | None:
        """Replace an existing workflow record with a new version."""
        with self._lock:
            user_records = workflow_engine_db.get(user_id)
            if user_records is None:
                return None

            normalized_id = normalize_workflow_id(workflow_id)
            if normalized_id not in user_records:
                return None

            new_normalized_id = normalize_workflow_id(record.workflow_id)
            if new_normalized_id != normalized_id:
                del user_records[normalized_id]

            user_records[new_normalized_id] = record

        return record

    def delete_record(
        self,
        user_id: str,
        workflow_id: str,
    ) -> WorkflowRecord | None:
        """Delete and return a workflow record by ID."""
        with self._lock:
            user_records = workflow_engine_db.get(user_id)
            if user_records is None:
                return None

            normalized_id = normalize_workflow_id(workflow_id)
            return user_records.pop(normalized_id, None)
