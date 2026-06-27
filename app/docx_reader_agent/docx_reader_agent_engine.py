"""DOCX Reader Agent with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.docx_reader_agent.schemas import DOCXReaderRecord

# In-memory DOCX reader store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "docx_id": "docx_001",
#             "docx_file": "project_proposal.docx",
#             "document_title": "Project Proposal 2025",
#             "page_count": 18,
#             "extracted_text": "This proposal outlines the scope and objectives...",
#             "summary": "Strategic project proposal with timeline and deliverables.",
#             "language": "en",
#             "confidence_score": 95,
#             "status": "completed",
#             "progress_percentage": 100,
#             "created_at": "2026-06-04T14:00:00",
#             "updated_at": "2026-06-04T14:08:00",
#         }
#     ]
# }
docx_reader_db: dict[str, list[DOCXReaderRecord]] = {}


def normalize_docx_id(docx_id: str) -> str:
    """Normalize a DOCX ID for case-insensitive, whitespace-tolerant lookups."""
    return docx_id.strip().lower()


class DOCXReaderAgentEngine:
    """Manage user DOCX reader records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def docx_id_exists(self, user_id: str, docx_id: str) -> bool:
        """Return True if a record for this DOCX ID already exists."""
        with self._lock:
            return self._find_record_index(
                docx_reader_db.get(user_id, []),
                docx_id,
            ) is not None

    def create_record(
        self,
        user_id: str,
        record: DOCXReaderRecord,
    ) -> DOCXReaderRecord:
        """Create and store a DOCX reader record for the given user."""
        with self._lock:
            user_records = docx_reader_db.setdefault(user_id, [])
            user_records.append(record)

        return record

    def get_records(self, user_id: str) -> list[DOCXReaderRecord]:
        """Return all DOCX reader records for the given user."""
        with self._lock:
            return list(docx_reader_db.get(user_id, []))

    def get_record(
        self,
        user_id: str,
        docx_id: str,
    ) -> DOCXReaderRecord | None:
        """Return one DOCX reader record by ID for the given user."""
        with self._lock:
            return self._find_record(user_id, docx_id)

    def update_record(
        self,
        user_id: str,
        docx_id: str,
        record: DOCXReaderRecord,
    ) -> DOCXReaderRecord | None:
        """Replace an existing DOCX reader record with a new version."""
        with self._lock:
            user_records = docx_reader_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, docx_id)
            if index is None:
                return None

            user_records[index] = record

        return record

    def delete_record(
        self,
        user_id: str,
        docx_id: str,
    ) -> DOCXReaderRecord | None:
        """Delete and return a DOCX reader record by ID."""
        with self._lock:
            user_records = docx_reader_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, docx_id)
            if index is None:
                return None

            return user_records.pop(index)

    def _find_record(
        self,
        user_id: str,
        docx_id: str,
    ) -> DOCXReaderRecord | None:
        """Locate a DOCX reader record in the user's list by ID."""
        user_records = docx_reader_db.get(user_id, [])
        index = self._find_record_index(user_records, docx_id)
        if index is None:
            return None
        return user_records[index]

    @staticmethod
    def _find_record_index(
        user_records: list[DOCXReaderRecord],
        docx_id: str,
    ) -> int | None:
        """Return the list index for a DOCX ID, if it exists."""
        normalized_id = normalize_docx_id(docx_id)
        for index, record in enumerate(user_records):
            if normalize_docx_id(record.docx_id) == normalized_id:
                return index
        return None
