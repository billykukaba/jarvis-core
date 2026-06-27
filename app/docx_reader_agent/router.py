"""FastAPI routes for the DOCX Reader Agent.

Reads Microsoft Word (.docx) documents, extracts text, metadata and summaries
for Jarvis Documentation Intelligence.
"""

from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, status

from app.docx_reader_agent.docx_reader_agent_engine import normalize_docx_id
from app.docx_reader_agent.schemas import (
    DOCXReaderRecord,
    DOCXReaderRecordResponse,
    UserDOCXReaderAgentResponse,
)
from app.services.engine_registry import docx_reader_agent_engine

# Router exposed to FastAPI as docx_reader_agent_router in main.py.
docx_reader_agent_router = APIRouter(tags=["DOCX Reader Agent"])


def parse_path_docx_id(docx_id: str) -> str:
    """Decode URL path DOCX IDs so spaces work in GET, PUT, and DELETE."""
    return unquote(docx_id.replace("+", " "))


@docx_reader_agent_router.post(
    "/docx_reader_agent/{user_id}",
    response_model=DOCXReaderRecordResponse,
    summary="Create DOCX reader record",
    description=(
        "Create a new DOCX reader record for the specified user. "
        "Reads Microsoft Word (.docx) documents, extracts text, metadata and "
        "summaries for Jarvis Documentation Intelligence."
    ),
)
async def create_docx_reader_record(
    user_id: str,
    request: DOCXReaderRecord,
) -> DOCXReaderRecordResponse:
    """Create and return a DOCX reader record."""
    if docx_reader_agent_engine.docx_id_exists(user_id, request.docx_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="DOCX reader record already exists",
        )

    record = docx_reader_agent_engine.create_record(user_id, request)
    return DOCXReaderRecordResponse.from_record(record)


@docx_reader_agent_router.get(
    "/docx_reader_agent/{user_id}",
    response_model=UserDOCXReaderAgentResponse,
    summary="Get all DOCX reader records",
    description=(
        "Return all DOCX reader records saved by the specified user. "
        "Reads Microsoft Word (.docx) documents, extracts text, metadata and "
        "summaries for Jarvis Documentation Intelligence."
    ),
)
async def get_docx_reader_records(
    user_id: str,
) -> UserDOCXReaderAgentResponse:
    """Return all DOCX reader records for a user."""
    records = docx_reader_agent_engine.get_records(user_id)
    return UserDOCXReaderAgentResponse(
        user_id=user_id,
        docx_reader_records=[
            DOCXReaderRecordResponse.from_record(record) for record in records
        ],
    )


@docx_reader_agent_router.get(
    "/docx_reader_agent/{user_id}/{docx_id}",
    response_model=DOCXReaderRecordResponse,
    summary="Get one DOCX reader record",
    description="Return one DOCX reader record identified by DOCX ID.",
)
async def get_docx_reader_record(
    user_id: str,
    docx_id: str,
) -> DOCXReaderRecordResponse:
    """Return a single DOCX reader record by ID."""
    decoded_id = parse_path_docx_id(docx_id)
    record = docx_reader_agent_engine.get_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="DOCX reader record not found",
        )

    return DOCXReaderRecordResponse.from_record(record)


@docx_reader_agent_router.put(
    "/docx_reader_agent/{user_id}/{docx_id}",
    response_model=DOCXReaderRecordResponse,
    status_code=status.HTTP_200_OK,
    summary="Update DOCX reader record",
    description="Replace an existing DOCX reader record with updated data.",
)
async def update_docx_reader_record(
    user_id: str,
    docx_id: str,
    request: DOCXReaderRecord,
) -> DOCXReaderRecordResponse:
    """Update and return a DOCX reader record."""
    decoded_id = parse_path_docx_id(docx_id)

    if normalize_docx_id(request.docx_id) != normalize_docx_id(decoded_id):
        if docx_reader_agent_engine.docx_id_exists(user_id, request.docx_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="DOCX reader record already exists",
            )

    record = docx_reader_agent_engine.update_record(
        user_id,
        decoded_id,
        request,
    )
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="DOCX reader record not found",
        )

    return DOCXReaderRecordResponse.from_record(record)


@docx_reader_agent_router.delete(
    "/docx_reader_agent/{user_id}/{docx_id}",
    response_model=DOCXReaderRecordResponse,
    summary="Delete DOCX reader record",
    description="Delete a DOCX reader record and return the removed record.",
)
async def delete_docx_reader_record(
    user_id: str,
    docx_id: str,
) -> DOCXReaderRecordResponse:
    """Delete a DOCX reader record and return the deleted item."""
    decoded_id = parse_path_docx_id(docx_id)
    record = docx_reader_agent_engine.delete_record(user_id, decoded_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="DOCX reader record not found",
        )

    return DOCXReaderRecordResponse.from_record(record)
