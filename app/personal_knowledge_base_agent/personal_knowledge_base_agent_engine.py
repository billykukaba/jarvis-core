"""Personal Knowledge Base Agent with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.personal_knowledge_base_agent.schemas import PersonalKnowledgeRecord

# In-memory personal knowledge base store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "knowledge_base_id": "kb_001",
#             "knowledge_title": "FastAPI Best Practices",
#             "knowledge_category": "programming",
#             "knowledge_content": "Use dependency injection and Pydantic models for validation.",
#             "knowledge_source": "internal_notes.md",
#             "related_tags": ["fastapi", "python", "api-design"],
#             "importance_score": 85,
#             "status": "active",
#             "progress_percentage": 100,
#             "created_at": "2026-06-04T17:00:00",
#             "updated_at": "2026-06-04T17:05:00",
#         }
#     ]
# }
personal_knowledge_base_db: dict[str, list[PersonalKnowledgeRecord]] = {}


def normalize_knowledge_base_id(knowledge_base_id: str) -> str:
    """Normalize a knowledge base ID for case-insensitive, whitespace-tolerant lookups."""
    return knowledge_base_id.strip().lower()


class PersonalKnowledgeBaseAgentEngine:
    """Manage user personal knowledge records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def knowledge_base_id_exists(
        self,
        user_id: str,
        knowledge_base_id: str,
    ) -> bool:
        """Return True if a record for this knowledge base ID already exists."""
        with self._lock:
            return self._find_record_index(
                personal_knowledge_base_db.get(user_id, []),
                knowledge_base_id,
            ) is not None

    def create_record(
        self,
        user_id: str,
        record: PersonalKnowledgeRecord,
    ) -> PersonalKnowledgeRecord:
        """Create and store a personal knowledge record for the given user."""
        with self._lock:
            user_records = personal_knowledge_base_db.setdefault(user_id, [])
            user_records.append(record)

        return record

    def get_records(self, user_id: str) -> list[PersonalKnowledgeRecord]:
        """Return all personal knowledge records for the given user."""
        with self._lock:
            return list(personal_knowledge_base_db.get(user_id, []))

    def get_record(
        self,
        user_id: str,
        knowledge_base_id: str,
    ) -> PersonalKnowledgeRecord | None:
        """Return one personal knowledge record by ID for the given user."""
        with self._lock:
            return self._find_record(user_id, knowledge_base_id)

    def update_record(
        self,
        user_id: str,
        knowledge_base_id: str,
        record: PersonalKnowledgeRecord,
    ) -> PersonalKnowledgeRecord | None:
        """Replace an existing personal knowledge record with a new version."""
        with self._lock:
            user_records = personal_knowledge_base_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, knowledge_base_id)
            if index is None:
                return None

            user_records[index] = record

        return record

    def delete_record(
        self,
        user_id: str,
        knowledge_base_id: str,
    ) -> PersonalKnowledgeRecord | None:
        """Delete and return a personal knowledge record by ID."""
        with self._lock:
            user_records = personal_knowledge_base_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, knowledge_base_id)
            if index is None:
                return None

            return user_records.pop(index)

    def _find_record(
        self,
        user_id: str,
        knowledge_base_id: str,
    ) -> PersonalKnowledgeRecord | None:
        """Locate a personal knowledge record in the user's list by ID."""
        user_records = personal_knowledge_base_db.get(user_id, [])
        index = self._find_record_index(user_records, knowledge_base_id)
        if index is None:
            return None
        return user_records[index]

    @staticmethod
    def _find_record_index(
        user_records: list[PersonalKnowledgeRecord],
        knowledge_base_id: str,
    ) -> int | None:
        """Return the list index for a knowledge base ID, if it exists."""
        normalized_id = normalize_knowledge_base_id(knowledge_base_id)
        for index, record in enumerate(user_records):
            if normalize_knowledge_base_id(record.knowledge_base_id) == normalized_id:
                return index
        return None
