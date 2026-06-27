"""Pydantic schemas for the File Knowledge Extraction Agent."""

from pydantic import BaseModel, ConfigDict, Field


class FileKnowledgeExtractionRecord(BaseModel):
    """File knowledge extraction record stored for a user."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "knowledge_id": "knowledge_001",
                    "file_name": "research_paper.pdf",
                    "file_type": "pdf",
                    "document_title": "AI Research Overview",
                    "extracted_knowledge": "Machine learning enables systems to learn from data...",
                    "keywords": ["machine learning", "neural networks", "NLP"],
                    "summary": "Overview of AI research trends and key concepts.",
                    "confidence_score": 92,
                    "status": "completed",
                    "progress_percentage": 100,
                    "created_at": "2026-06-04T16:00:00",
                    "updated_at": "2026-06-04T16:08:00",
                }
            ]
        }
    )

    knowledge_id: str = Field(
        min_length=1,
        description="Unique knowledge extraction record identifier",
        examples=["knowledge_001"],
    )
    file_name: str = Field(
        min_length=1,
        description="Source file name or path",
        examples=["research_paper.pdf"],
    )
    file_type: str = Field(
        min_length=1,
        description="Type of the source file",
        examples=["pdf"],
    )
    document_title: str = Field(
        min_length=1,
        description="Title of the source document",
        examples=["AI Research Overview"],
    )
    extracted_knowledge: str = Field(
        min_length=1,
        description="Structured knowledge extracted from the document",
        examples=["Machine learning enables systems to learn from data..."],
    )
    keywords: list[str] = Field(
        min_length=1,
        description="Keywords identified in the document",
        examples=[["machine learning", "neural networks", "NLP"]],
    )
    summary: str = Field(
        min_length=1,
        description="Summary of the extracted knowledge",
        examples=["Overview of AI research trends and key concepts."],
    )
    confidence_score: int = Field(
        ge=0,
        le=100,
        description="Knowledge extraction confidence score",
        examples=[92],
    )
    status: str = Field(
        min_length=1,
        description="Current knowledge extraction status",
        examples=["completed"],
    )
    progress_percentage: int = Field(
        ge=0,
        le=100,
        description="Knowledge extraction progress percentage",
        examples=[100],
    )
    created_at: str = Field(
        min_length=1,
        description="Record creation timestamp",
        examples=["2026-06-04T16:00:00"],
    )
    updated_at: str = Field(
        min_length=1,
        description="Record last update timestamp",
        examples=["2026-06-04T16:08:00"],
    )


class FileKnowledgeExtractionRecordResponse(BaseModel):
    """File knowledge extraction record returned by the API."""

    knowledge_id: str
    file_name: str
    file_type: str
    document_title: str
    extracted_knowledge: str
    keywords: list[str]
    summary: str
    confidence_score: int
    status: str
    progress_percentage: int
    created_at: str
    updated_at: str

    @classmethod
    def from_record(
        cls,
        record: FileKnowledgeExtractionRecord,
    ) -> "FileKnowledgeExtractionRecordResponse":
        """Build an API response from a stored knowledge extraction record."""
        return cls(
            knowledge_id=record.knowledge_id,
            file_name=record.file_name,
            file_type=record.file_type,
            document_title=record.document_title,
            extracted_knowledge=record.extracted_knowledge,
            keywords=record.keywords,
            summary=record.summary,
            confidence_score=record.confidence_score,
            status=record.status,
            progress_percentage=record.progress_percentage,
            created_at=record.created_at,
            updated_at=record.updated_at,
        )


class UserFileKnowledgeExtractionAgentResponse(BaseModel):
    """All file knowledge extraction records for one user."""

    user_id: str
    knowledge_records: list[FileKnowledgeExtractionRecordResponse]
