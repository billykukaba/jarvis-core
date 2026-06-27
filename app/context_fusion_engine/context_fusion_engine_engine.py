"""Context Fusion Engine with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.context_fusion_engine.schemas import ContextFusionRecord

# In-memory context fusion store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "fusion_id": "fusion_001",
#             "context_sources": [
#                 "conversation_history",
#                 "long_term_memory",
#                 "user_goals",
#                 "emotional_state",
#             ],
#             "current_context": "User is planning a product launch meeting.",
#             "long_term_memory_context": "User prefers concise technical summaries.",
#             "user_goal_context": "Prepare launch timeline and stakeholder updates.",
#             "emotional_context": "Focused and motivated.",
#             "fusion_summary": "User needs a structured launch plan with technical clarity.",
#             "confidence_score": 91,
#             "status": "completed",
#             "progress_percentage": 100,
#             "created_at": "2026-06-05T03:00:00",
#             "updated_at": "2026-06-05T03:08:00",
#         }
#     ]
# }
context_fusion_engine_db: dict[str, list[ContextFusionRecord]] = {}


def normalize_fusion_id(fusion_id: str) -> str:
    """Normalize a fusion ID for case-insensitive, whitespace-tolerant lookups."""
    return fusion_id.strip().lower()


class ContextFusionEngine:
    """Manage user context fusion records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def fusion_id_exists(self, user_id: str, fusion_id: str) -> bool:
        """Return True if a record for this fusion ID already exists."""
        with self._lock:
            return self._find_record_index(
                context_fusion_engine_db.get(user_id, []),
                fusion_id,
            ) is not None

    def create_record(
        self,
        user_id: str,
        record: ContextFusionRecord,
    ) -> ContextFusionRecord:
        """Create and store a context fusion record for the given user."""
        with self._lock:
            user_records = context_fusion_engine_db.setdefault(user_id, [])
            user_records.append(record)

        return record

    def get_records(self, user_id: str) -> list[ContextFusionRecord]:
        """Return all context fusion records for the given user."""
        with self._lock:
            return list(context_fusion_engine_db.get(user_id, []))

    def get_record(
        self,
        user_id: str,
        fusion_id: str,
    ) -> ContextFusionRecord | None:
        """Return one context fusion record by ID for the given user."""
        with self._lock:
            return self._find_record(user_id, fusion_id)

    def update_record(
        self,
        user_id: str,
        fusion_id: str,
        record: ContextFusionRecord,
    ) -> ContextFusionRecord | None:
        """Replace an existing context fusion record with a new version."""
        with self._lock:
            user_records = context_fusion_engine_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, fusion_id)
            if index is None:
                return None

            user_records[index] = record

        return record

    def delete_record(
        self,
        user_id: str,
        fusion_id: str,
    ) -> ContextFusionRecord | None:
        """Delete and return a context fusion record by ID."""
        with self._lock:
            user_records = context_fusion_engine_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, fusion_id)
            if index is None:
                return None

            return user_records.pop(index)

    def _find_record(
        self,
        user_id: str,
        fusion_id: str,
    ) -> ContextFusionRecord | None:
        """Locate a context fusion record in the user's list by ID."""
        user_records = context_fusion_engine_db.get(user_id, [])
        index = self._find_record_index(user_records, fusion_id)
        if index is None:
            return None
        return user_records[index]

    @staticmethod
    def _find_record_index(
        user_records: list[ContextFusionRecord],
        fusion_id: str,
    ) -> int | None:
        """Return the list index for a fusion ID, if it exists."""
        normalized_id = normalize_fusion_id(fusion_id)
        for index, record in enumerate(user_records):
            if normalize_fusion_id(record.fusion_id) == normalized_id:
                return index
        return None
