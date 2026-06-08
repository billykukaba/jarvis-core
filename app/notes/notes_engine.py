from __future__ import annotations

from threading import Lock

from app.notes.schemas import Note

notes_db: dict[str, list[Note]] = {}


class NotesEngine:
    def __init__(self) -> None:
        self._lock = Lock()

    def create_note(self, user_id: str, note: Note) -> Note:
        with self._lock:
            user_notes = notes_db.setdefault(user_id, [])
            user_notes.append(note)

        return note

    def get_notes(self, user_id: str) -> list[Note]:
        with self._lock:
            return list(notes_db.get(user_id, []))

    def get_note(self, user_id: str, title: str) -> Note | None:
        with self._lock:
            return self._find_note(user_id, title)

    def update_note(self, user_id: str, title: str, note: Note) -> Note | None:
        with self._lock:
            user_notes = notes_db.get(user_id)
            if user_notes is None:
                return None

            index = self._find_note_index(user_notes, title)
            if index is None:
                return None

            user_notes[index] = note

        return note

    def delete_note(self, user_id: str, title: str) -> Note | None:
        with self._lock:
            user_notes = notes_db.get(user_id)
            if user_notes is None:
                return None

            index = self._find_note_index(user_notes, title)
            if index is None:
                return None

            return user_notes.pop(index)

    def _find_note(self, user_id: str, title: str) -> Note | None:
        user_notes = notes_db.get(user_id, [])
        index = self._find_note_index(user_notes, title)
        if index is None:
            return None
        return user_notes[index]

    @staticmethod
    def _find_note_index(user_notes: list[Note], title: str) -> int | None:
        normalized_title = title.lower()
        for index, note in enumerate(user_notes):
            if note.title.lower() == normalized_title:
                return index
        return None
