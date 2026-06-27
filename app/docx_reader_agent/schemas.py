"""Pydantic schemas for the DOCX Reader Agent."""

from pydantic import BaseModel, ConfigDict, Field


class DOCXReaderRecord(BaseModel):
    """DOCX reader record stored for a user."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "docx_id": "docx_001",
                    "docx_file": "project_proposal.docx",
                    "document_title": "Project Proposal 2025",
                    "page_count": 18,
                    "extracted_text": "This proposal outlines the scope and objectives...",
                    "summary": "Strategic project proposal with timeline and deliverables.",
                    "language": "en",
                    "confidence_score": 95,
                    "status": "completed",
                    "progress_percentage": 100,
                    "created_at": "2026-06-04T14:00:00",
                    "updated_at": "2026-06-04T14:08:00",
                }
            ]
        }
    )

    docx_id: str = Field(
        min_length=1,
        description="Unique DOCX reader record identifier",
        examples=["docx_001"],
    )
    docx_file: str = Field(
        min_length=1,
        description="DOCX file name or path",
        examples=["project_proposal.docx"],
    )
    document_title: str = Field(
        min_length=1,
        description="Title of the DOCX document",
        examples=["Project Proposal 2025"],
    )
    page_count: int = Field(
        ge=0,
        description="Total number of pages in the DOCX document",
        examples=[18],
    )
    extracted_text: str = Field(
        min_length=1,
        description="Text extracted from the DOCX document",
        examples=["This proposal outlines the scope and objectives..."],
    )
    summary: str = Field(
        min_length=1,
        description="Summary of the DOCX document content",
        examples=["Strategic project proposal with timeline and deliverables."],
    )
    language: str = Field(
        min_length=1,
        description="Detected language of the DOCX content",
        examples=["en"],
    )
    confidence_score: int = Field(
        ge=0,
        le=100,
        description="DOCX reading and extraction confidence score",
        examples=[95],
    )
    status: str = Field(
        min_length=1,
        description="Current DOCX reading status",
        examples=["completed"],
    )
    progress_percentage: int = Field(
        ge=0,
        le=100,
        description="DOCX reading progress percentage",
        examples=[100],
    )
    created_at: str = Field(
        min_length=1,
        description="Record creation timestamp",
        examples=["2026-06-04T14:00:00"],
    )
    updated_at: str = Field(
        min_length=1,
        description="Record last update timestamp",
        examples=["2026-06-04T14:08:00"],
    )


class DOCXReaderRecordResponse(BaseModel):
    """DOCX reader record returned by the API."""

    docx_id: str
    docx_file: str
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
    def from_record(
        cls,
        record: DOCXReaderRecord,
    ) -> "DOCXReaderRecordResponse":
        """Build an API response from a stored DOCX reader record."""
        return cls(
            docx_id=record.docx_id,
            docx_file=record.docx_file,
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


class UserDOCXReaderAgentResponse(BaseModel):
    """All DOCX reader records for one user."""

    user_id: str
    docx_reader_records: list[DOCXReaderRecordResponse]
