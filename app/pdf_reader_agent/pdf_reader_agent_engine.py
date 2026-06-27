"""PDF Reader Agent with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.pdf_reader_agent.schemas import PDFReaderRecord

# In-memory PDF reader store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "pdf_id": "pdf_001",
#             "pdf_file": "annual_report_2025.pdf",
#             "document_title": "Annual Report 2025",
#             "page_count": 42,
#             "extracted_text": "This annual report summarizes company performance...",
#             "summary": "Financial overview and strategic highlights for fiscal year 2025.",
#             "language": "en",
#             "confidence_score": 96,
#             "status": "completed",
#             "progress_percentage": 100,
#             "created_at": "2026-06-04T13:00:00",
#             "updated_at": "2026-06-04T13:10:00",
#         }
#     ]
# }
pdf_reader_db: dict[str, list[PDFReaderRecord]] = {}


def normalize_pdf_id(pdf_id: str) -> str:
    """Normalize a PDF ID for case-insensitive, whitespace-tolerant lookups."""
    return pdf_id.strip().lower()


class PDFReaderAgentEngine:
    """Manage user PDF reader records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def pdf_id_exists(self, user_id: str, pdf_id: str) -> bool:
        """Return True if a record for this PDF ID already exists."""
        with self._lock:
            return self._find_record_index(
                pdf_reader_db.get(user_id, []),
                pdf_id,
            ) is not None

    def create_record(
        self,
        user_id: str,
        record: PDFReaderRecord,
    ) -> PDFReaderRecord:
        """Create and store a PDF reader record for the given user."""
        with self._lock:
            user_records = pdf_reader_db.setdefault(user_id, [])
            user_records.append(record)

        return record

    def get_records(self, user_id: str) -> list[PDFReaderRecord]:
        """Return all PDF reader records for the given user."""
        with self._lock:
            return list(pdf_reader_db.get(user_id, []))

    def get_record(
        self,
        user_id: str,
        pdf_id: str,
    ) -> PDFReaderRecord | None:
        """Return one PDF reader record by ID for the given user."""
        with self._lock:
            return self._find_record(user_id, pdf_id)

    def update_record(
        self,
        user_id: str,
        pdf_id: str,
        record: PDFReaderRecord,
    ) -> PDFReaderRecord | None:
        """Replace an existing PDF reader record with a new version."""
        with self._lock:
            user_records = pdf_reader_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, pdf_id)
            if index is None:
                return None

            user_records[index] = record

        return record

    def delete_record(
        self,
        user_id: str,
        pdf_id: str,
    ) -> PDFReaderRecord | None:
        """Delete and return a PDF reader record by ID."""
        with self._lock:
            user_records = pdf_reader_db.get(user_id)
            if user_records is None:
                return None

            index = self._find_record_index(user_records, pdf_id)
            if index is None:
                return None

            return user_records.pop(index)

    def _find_record(
        self,
        user_id: str,
        pdf_id: str,
    ) -> PDFReaderRecord | None:
        """Locate a PDF reader record in the user's list by ID."""
        user_records = pdf_reader_db.get(user_id, [])
        index = self._find_record_index(user_records, pdf_id)
        if index is None:
            return None
        return user_records[index]

    @staticmethod
    def _find_record_index(
        user_records: list[PDFReaderRecord],
        pdf_id: str,
    ) -> int | None:
        """Return the list index for a PDF ID, if it exists."""
        normalized_id = normalize_pdf_id(pdf_id)
        for index, record in enumerate(user_records):
            if normalize_pdf_id(record.pdf_id) == normalized_id:
                return index
        return None
