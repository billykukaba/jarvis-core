"""FastAPI routes for the Journal Service."""

from fastapi import APIRouter, HTTPException, status

from app.journals.schemas import (
    JournalEntry,
    JournalEntryResponse,
    UserJournalEntriesResponse,
)
from app.services.engine_registry import journal_service_engine

# Router exposed to FastAPI as journals_router in main.py.
journals_router = APIRouter(tags=["journals"])


@journals_router.post(
    "/journals/{user_id}",
    response_model=JournalEntryResponse,
    summary="Create journal entry",
    description="Create a new journal entry for the specified user.",
)
async def create_journal_entry(
    user_id: str,
    request: JournalEntry,
) -> JournalEntryResponse:
    """Create and return a journal entry."""
    entry = journal_service_engine.create_entry(user_id, request)
    return JournalEntryResponse.from_entry(entry)


@journals_router.get(
    "/journals/{user_id}",
    response_model=UserJournalEntriesResponse,
    summary="Get all journal entries",
    description="Return all journal entries saved by the specified user.",
)
async def get_journal_entries(user_id: str) -> UserJournalEntriesResponse:
    """Return all journal entries for a user."""
    entries = journal_service_engine.get_entries(user_id)
    return UserJournalEntriesResponse(
        user_id=user_id,
        entries=[JournalEntryResponse.from_entry(entry) for entry in entries],
    )


@journals_router.get(
    "/journals/{user_id}/{title}",
    response_model=JournalEntryResponse,
    summary="Get one journal entry",
    description="Return one journal entry identified by its title.",
)
async def get_journal_entry(user_id: str, title: str) -> JournalEntryResponse:
    """Return a single journal entry by title."""
    entry = journal_service_engine.get_entry(user_id, title)
    if entry is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Journal entry not found",
        )

    return JournalEntryResponse.from_entry(entry)


@journals_router.put(
    "/journals/{user_id}/{title}",
    response_model=JournalEntryResponse,
    summary="Update journal entry",
    description="Replace an existing journal entry with updated data.",
)
async def update_journal_entry(
    user_id: str,
    title: str,
    request: JournalEntry,
) -> JournalEntryResponse:
    """Update and return a journal entry."""
    entry = journal_service_engine.update_entry(user_id, title, request)
    if entry is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Journal entry not found",
        )

    return JournalEntryResponse.from_entry(entry)


@journals_router.delete(
    "/journals/{user_id}/{title}",
    response_model=JournalEntryResponse,
    summary="Delete journal entry",
    description="Delete a journal entry and return the removed entry.",
)
async def delete_journal_entry(user_id: str, title: str) -> JournalEntryResponse:
    """Delete a journal entry and return the deleted item."""
    entry = journal_service_engine.delete_entry(user_id, title)
    if entry is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Journal entry not found",
        )

    return JournalEntryResponse.from_entry(entry)
