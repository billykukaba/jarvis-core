"""File Knowledge Extraction Agent with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.file_knowledge_extraction_agent.schemas import FileKnowledgeExtractionRecord

# In-memory file knowledge extraction store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "knowledge_id": "knowledge_001",
#             "file_name": "research_paper.pdf",
#             "file_type": "pdf",
#             "document_title": "AI Research Overview",
#             "extracted_knowledge": "Machine learning enables systems to learn from data...",
#             "keywords": ["machine learning", "neural networks", "NLP"],
#             "summary": "Overview of AI research trends and key concepts.",
#             "confidence_score": 92,
#             "status": "completed",
#             "progress_percentage": 100,
#             "created_at": "2026-06-04T16:00:00",
#             "updated_at": "2026-06-04T16:08:00",
#         }
#     ]
# }
file_knowledge_extraction_db: dict[str, list[FileKnowledgeExtractionRecord]] = {}


def normalize_knowledge_id(knowledge_id: str) -> str:
    """Normalize a knowledge ID for case-insensitive, whitespace-tolerant lookups."""
    return knowledge_id.strip().lower()


class FileKnowledgeExtractionAgentEngine:
    """Manage user file knowledge extraction records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def knowledge_id_exists(self, user_id: str, knowledge_id: str) -> bool:
        """Return True if a record for this knowledge ID already exists."""
        with self._lock:
            return self._find_record_index(
                file_knowledge_extraction_db.get(user_id, []),
                knowledge_id,
            ) is not None

    def create_record(
        self,
        user_id: str,
        record: FileKnowledgeExtractionRecord,
    ) -> FileKnowledgeExtractionRecord:
        """Create and store a knowledge extraction record for the given user."""
        with self._lock:
            user_records = file_knowledge_extraction_db.setdefault(user_id, [])
            user_records.append(record)

        return record

    def get_records(self, user_id: str) -> list[FileKnowledgeExtractionRecord]:
        """Return all knowledge extraction records for the given user."""
        with self._lock:
            return list(file_knowledge_extraction_db.get(user_id, []))

    def get_record(
        self,
        user_id: str,
        knowledge_id: str,
    ) -> FileKnowledgeExtractionRecord | None:
        """Return one knowledge extraction record by ID for the given user."""
        with self._lock:
            return self._find_record(user_id, knowledge_id)

    def update_record(
        self,
        user_id: str,
        knowledge_id: str,
        record: FileKnowledgeExtractionRecord,
    ) -> FileKnowledgeExtractionRecord | None:
        """Replace an existing knowledge extraction record with a new version."""
        with self._lock:
            user_records = file_knowledge_extraction_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, knowledge_id)
            if index is None:
                return None

            user_records[index] = record

        return record

    def delete_record(
        self,
        user_id: str,
        knowledge_id: str,
    ) -> FileKnowledgeExtractionRecord | None:
        """Delete and return a knowledge extraction record by ID."""
        with self._lock:
            user_records = file_knowledge_extraction_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, knowledge_id)
            if index is None:
                return None

            return user_records.pop(index)

    def _find_record(
        self,
        user_id: str,
        knowledge_id: str,
    ) -> FileKnowledgeExtractionRecord | None:
        """Locate a knowledge extraction record in the user's list by ID."""
        user_records = file_knowledge_extraction_db.get(user_id, [])
        index = self._find_record_index(user_records, knowledge_id)
        if index is None:
            return None
        return user_records[index]

    @staticmethod
    def _find_record_index(
        user_records: list[FileKnowledgeExtractionRecord],
        knowledge_id: str,
    ) -> int | None:
        """Return the list index for a knowledge ID, if it exists."""
        normalized_id = normalize_knowledge_id(knowledge_id)
        for index, record in enumerate(user_records):
            if normalize_knowledge_id(record.knowledge_id) == normalized_id:
                return index
        return None
