"""Project Manager Agent with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.project_manager_agent.schemas import ProjectRecord

# In-memory project store keyed by user_id, then project_id.
# Example:
# {
#     "billy": {
#         "proj_001": {
#             "project_id": "proj_001",
#             "project_name": "Website Redesign",
#             "description": "Redesign the company website for improved UX",
#             "objectives": ["Audit current site", "Design new layout", "Launch updated site"],
#             "team_members": ["alice", "bob", "carol"],
#             "status": "in_progress",
#             "priority_level": 1,
#             "completion_percentage": 35,
#             "deadline": "2026-08-01",
#             "created_at": "2026-06-04T09:00:00",
#             "updated_at": "2026-06-04T10:30:00",
#         }
#     }
# }
project_manager_agent_db: dict[str, dict[str, ProjectRecord]] = {}


def normalize_project_id(project_id: str) -> str:
    """Normalize a project ID for case-insensitive, whitespace-tolerant lookups."""
    return project_id.strip().lower()


class ProjectManagerAgentEngine:
    """Manage user project records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def project_id_exists(self, user_id: str, project_id: str) -> bool:
        """Return True if a record for this project ID already exists."""
        with self._lock:
            user_records = project_manager_agent_db.get(user_id, {})
            return normalize_project_id(project_id) in user_records

    def create_record(self, user_id: str, record: ProjectRecord) -> ProjectRecord:
        """Create and store a project record for the given user."""
        with self._lock:
            user_records = project_manager_agent_db.setdefault(user_id, {})
            user_records[normalize_project_id(record.project_id)] = record

        return record

    def get_records(self, user_id: str) -> list[ProjectRecord]:
        """Return all project records for the given user."""
        with self._lock:
            user_records = project_manager_agent_db.get(user_id, {})
            return list(user_records.values())

    def get_record(self, user_id: str, project_id: str) -> ProjectRecord | None:
        """Return one project record by ID for the given user."""
        with self._lock:
            user_records = project_manager_agent_db.get(user_id, {})
            return user_records.get(normalize_project_id(project_id))

    def update_record(
        self,
        user_id: str,
        project_id: str,
        record: ProjectRecord,
    ) -> ProjectRecord | None:
        """Replace an existing project record with a new version."""
        with self._lock:
            user_records = project_manager_agent_db.get(user_id)
            if user_records is None:
                return None

            normalized_id = normalize_project_id(project_id)
            if normalized_id not in user_records:
                return None

            new_normalized_id = normalize_project_id(record.project_id)
            if new_normalized_id != normalized_id:
                del user_records[normalized_id]

            user_records[new_normalized_id] = record

        return record

    def delete_record(
        self,
        user_id: str,
        project_id: str,
    ) -> ProjectRecord | None:
        """Delete and return a project record by ID."""
        with self._lock:
            user_records = project_manager_agent_db.get(user_id)
            if user_records is None:
                return None

            normalized_id = normalize_project_id(project_id)
            return user_records.pop(normalized_id, None)
