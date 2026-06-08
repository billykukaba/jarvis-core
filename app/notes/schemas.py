from pydantic import BaseModel, Field


class Note(BaseModel):
    title: str = Field(min_length=1)
    content: str = Field(min_length=1)
    category: str = Field(min_length=1)


class NoteResponse(BaseModel):
    title: str
    content: str
    category: str

    @classmethod
    def from_note(cls, note: Note) -> "NoteResponse":
        return cls(
            title=note.title,
            content=note.content,
            category=note.category,
        )


class UserNotesResponse(BaseModel):
    user_id: str
    notes: list[NoteResponse]
