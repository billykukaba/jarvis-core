"""Pydantic schemas for the PDF Reader Agent."""

from pydantic import BaseModel, ConfigDict, Field


class PDFReaderRecord(BaseModel):
    """PDF reader record stored for a user."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "pdf_id": "pdf_001",
                    "pdf_file": "annual_report_2025.pdf",
                    "document_title": "Annual Report 2025",
                    "page_count": 42,
                    "extracted_text": "This annual report summarizes company performance...",
                    "summary": "Financial overview and strategic highlights for fiscal year 2025.",
                    "language": "en",
                    "confidence_score": 96,
                    "status": "completed",
                    "progress_percentage": 100,
                    "created_at": "2026-06-04T13:00:00",
                    "updated_at": "2026-06-04T13:10:00",
                }
            ]
        }
    )

    pdf_id: str = Field(
        min_length=1,
        description="Unique PDF reader record identifier",
        examples=["pdf_001"],
    )
    pdf_file: str = Field(
        min_length=1,
        description="PDF file name or path",
        examples=["annual_report_2025.pdf"],
    )
    document_title: str = Field(
        min_length=1,
        description="Title of the PDF document",
        examples=["Annual Report 2025"],
    )
    page_count: int = Field(
        ge=0,
        description="Total number of pages in the PDF document",
        examples=[42],
    )
    extracted_text: str = Field(
        min_length=1,
        description="Text extracted from the PDF document",
        examples=["This annual report summarizes company performance..."],
    )
    summary: str = Field(
        min_length=1,
        description="Summary of the PDF document content",
        examples=["Financial overview and strategic highlights for fiscal year 2025."],
    )
    language: str = Field(
        min_length=1,
        description="Detected language of the PDF content",
        examples=["en"],
    )
    confidence_score: int = Field(
        ge=0,
        le=100,
        description="PDF reading and extraction confidence score",
        examples=[96],
    )
    status: str = Field(
        min_length=1,
        description="Current PDF reading status",
        examples=["completed"],
    )
    progress_percentage: int = Field(
        ge=0,
        le=100,
        description="PDF reading progress percentage",
        examples=[100],
    )
    created_at: str = Field(
        min_length=1,
        description="Record creation timestamp",
        examples=["2026-06-04T13:00:00"],
    )
    updated_at: str = Field(
        min_length=1,
        description="Record last update timestamp",
        examples=["2026-06-04T13:10:00"],
    )


class PDFReaderRecordResponse(BaseModel):
    """PDF reader record returned by the API."""

    pdf_id: str
    pdf_file: str
    document_title: str
    page_count: int
    extracted_text: str
    summary: str
    language: str
    confidence_score: int
    status: str
    progress_percentage: int
    created_at: str
    updated_at: str

    @classmethod
    def from_record(cls, record: PDFReaderRecord) -> "PDFReaderRecordResponse":
        """Build an API response from a stored PDF reader record."""
        return cls(
            pdf_id=record.pdf_id,
            pdf_file=record.pdf_file,
            document_title=record.document_title,
            page_count=record.page_count,
            extracted_text=record.extracted_text,
            summary=record.summary,
            language=record.language,
            confidence_score=record.confidence_score,
            status=record.status,
            progress_percentage=record.progress_percentage,
            created_at=record.created_at,
            updated_at=record.updated_at,
        )


class UserPDFReaderAgentResponse(BaseModel):
    """All PDF reader records for one user."""

    user_id: str
    pdf_reader_records: list[PDFReaderRecordResponse]
