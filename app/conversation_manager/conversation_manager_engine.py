"""Conversation Manager engine with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.conversation_manager.schemas import ConversationManagerRecord

# In-memory conversation store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "conversation_id": "conv-001",
#             "title": "MIT Planning",
#             "status": "active",
#         }
#     ]
# }
conversation_manager_db: dict[str, list[ConversationManagerRecord]] = {}


def normalize_conversation_id(conversation_id: str) -> str:
    """Normalize a conversation ID for case-insensitive, whitespace-tolerant lookups."""
    return conversation_id.strip().lower()


class ConversationManagerEngine:
    """Manage user conversation records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def conversation_id_exists(self, user_id: str, conversation_id: str) -> bool:
        """Return True if a record for this conversation ID already exists."""
        with self._lock:
            return self._find_record_index(
                conversation_manager_db.get(user_id, []),
                conversation_id,
            ) is not None

    def create_record(
        self,
        user_id: str,
        record: ConversationManagerRecord,
    ) -> ConversationManagerRecord:
        """Create and store a conversation record for the given user."""
        with self._lock:
            user_records = conversation_manager_db.setdefault(user_id, [])
            user_records.append(record)

        return record

    def get_records(self, user_id: str) -> list[ConversationManagerRecord]:
        """Return all conversation records for the given user."""
        with self._lock:
            return list(conversation_manager_db.get(user_id, []))

    def get_record(
        self,
        user_id: str,
        conversation_id: str,
    ) -> ConversationManagerRecord | None:
        """Return one conversation record by ID for the given user."""
        with self._lock:
            return self._find_record(user_id, conversation_id)

    def update_record(
        self,
        user_id: str,
        conversation_id: str,
        record: ConversationManagerRecord,
    ) -> ConversationManagerRecord | None:
        """Replace an existing conversation record with a new version."""
        with self._lock:
            user_records = conversation_manager_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, conversation_id)
            if index is None:
                return None

            user_records[index] = record

        return record

    def delete_record(
        self,
        user_id: str,
        conversation_id: str,
    ) -> ConversationManagerRecord | None:
        """Delete and return a conversation record by ID."""
        with self._lock:
            user_records = conversation_manager_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, conversation_id)
            if index is None:
                return None

            return user_records.pop(index)

    def _find_record(
        self,
        user_id: str,
        conversation_id: str,
    ) -> ConversationManagerRecord | None:
        """Locate a conversation record in the user's list by ID."""
        user_records = conversation_manager_db.get(user_id, [])
        index = self._find_record_index(user_records, conversation_id)
        if index is None:
            return None
        return user_records[index]

    @staticmethod
    def _find_record_index(
        user_records: list[ConversationManagerRecord],
        conversation_id: str,
    ) -> int | None:
        """Return the list index for a conversation ID, if it exists."""
        normalized_id = normalize_conversation_id(conversation_id)
        for index, record in enumerate(user_records):
            if normalize_conversation_id(record.conversation_id) == normalized_id:
                return index
        return None
