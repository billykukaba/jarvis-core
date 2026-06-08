from fastapi import APIRouter, HTTPException, status

from app.notes.schemas import Note, NoteResponse, UserNotesResponse
from app.services.engine_registry import notes_engine

router = APIRouter(tags=["Notes System"])


@router.post(
    "/notes/{user_id}",
    response_model=NoteResponse,
    summary="Create a personal note",
    description="Create a new note for the specified user.",
)
async def create_note(user_id: str, request: Note) -> NoteResponse:
    note = notes_engine.create_note(user_id, request)
    return NoteResponse.from_note(note)


@router.get(
    "/notes/{user_id}",
    response_model=UserNotesResponse,
    summary="Get all notes",
    description="Return all personal notes for the specified user.",
)
async def get_notes(user_id: str) -> UserNotesResponse:
    notes = notes_engine.get_notes(user_id)
    return UserNotesResponse(
        user_id=user_id,
        notes=[NoteResponse.from_note(note) for note in notes],
    )


@router.get(
    "/notes/{user_id}/{title}",
    response_model=NoteResponse,
    summary="Get a single note",
    description="Return one note by title for the specified user.",
)
async def get_note(user_id: str, title: str) -> NoteResponse:
    note = notes_engine.get_note(user_id, title)
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )

    return NoteResponse.from_note(note)


@router.put(
    "/notes/{user_id}/{title}",
    response_model=NoteResponse,
    summary="Update a note",
    description="Replace an existing note with a new version.",
)
async def update_note(user_id: str, title: str, request: Note) -> NoteResponse:
    note = notes_engine.update_note(user_id, title, request)
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )

    return NoteResponse.from_note(note)


@router.delete(
    "/notes/{user_id}/{title}",
    response_model=NoteResponse,
    summary="Delete a note",
    description="Delete a note and return the removed note.",
)
async def delete_note(user_id: str, title: str) -> NoteResponse:
    note = notes_engine.delete_note(user_id, title)
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )

    return NoteResponse.from_note(note)
