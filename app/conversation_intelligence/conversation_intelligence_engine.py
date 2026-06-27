"""Conversation Intelligence engine with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.conversation_intelligence.schemas import ConversationIntelligenceRecord

# In-memory conversation intelligence store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "intelligence_id": "intel_001",
#             "sentiment": "Positive",
#             "summary": "User discussed AI project planning",
#         }
#     ]
# }
conversation_intelligence_db: dict[str, list[ConversationIntelligenceRecord]] = {}


def normalize_intelligence_id(intelligence_id: str) -> str:
    """Normalize an intelligence ID for case-insensitive, whitespace-tolerant lookups."""
    return intelligence_id.strip().lower()


class ConversationIntelligenceEngine:
    """Manage user conversation intelligence records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def intelligence_id_exists(self, user_id: str, intelligence_id: str) -> bool:
        """Return True if a record for this intelligence ID already exists."""
        with self._lock:
            return self._find_record_index(
                conversation_intelligence_db.get(user_id, []),
                intelligence_id,
            ) is not None

    def create_record(
        self,
        user_id: str,
        record: ConversationIntelligenceRecord,
    ) -> ConversationIntelligenceRecord:
        """Create and store an intelligence record for the given user."""
        with self._lock:
            user_records = conversation_intelligence_db.setdefault(user_id, [])
            user_records.append(record)

        return record

    def get_records(self, user_id: str) -> list[ConversationIntelligenceRecord]:
        """Return all intelligence records for the given user."""
        with self._lock:
            return list(conversation_intelligence_db.get(user_id, []))

    def get_record(
        self,
        user_id: str,
        intelligence_id: str,
    ) -> ConversationIntelligenceRecord | None:
        """Return one intelligence record by ID for the given user."""
        with self._lock:
            return self._find_record(user_id, intelligence_id)

    def update_record(
        self,
        user_id: str,
        intelligence_id: str,
        record: ConversationIntelligenceRecord,
    ) -> ConversationIntelligenceRecord | None:
        """Replace an existing intelligence record with a new version."""
        with self._lock:
            user_records = conversation_intelligence_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, intelligence_id)
            if index is None:
                return None

            user_records[index] = record

        return record

    def delete_record(
        self,
        user_id: str,
        intelligence_id: str,
    ) -> ConversationIntelligenceRecord | None:
        """Delete and return an intelligence record by ID."""
        with self._lock:
            user_records = conversation_intelligence_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, intelligence_id)
            if index is None:
                return None

            return user_records.pop(index)

    def _find_record(
        self,
        user_id: str,
        intelligence_id: str,
    ) -> ConversationIntelligenceRecord | None:
        """Locate an intelligence record in the user's list by ID."""
        user_records = conversation_intelligence_db.get(user_id, [])
        index = self._find_record_index(user_records, intelligence_id)
        if index is None:
            return None
        return user_records[index]

    @staticmethod
    def _find_record_index(
        user_records: list[ConversationIntelligenceRecord],
        intelligence_id: str,
    ) -> int | None:
        """Return the list index for an intelligence ID, if it exists."""
        normalized_id = normalize_intelligence_id(intelligence_id)
        for index, record in enumerate(user_records):
            if normalize_intelligence_id(record.intelligence_id) == normalized_id:
                return index
        return None
