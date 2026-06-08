from pydantic import BaseModel, Field

from app.context.context_engine import UserContext


class ContextRequest(BaseModel):
    current_topic: str = Field(min_length=1)
    current_task: str = Field(min_length=1)
    current_project: str = Field(min_length=1)
    notes: str = Field(min_length=1)

    def to_context(self) -> UserContext:
        return UserContext(
            current_topic=self.current_topic,
            current_task=self.current_task,
            current_project=self.current_project,
            notes=self.notes,
        )


class ContextResponse(BaseModel):
    user_id: str
    current_topic: str
    current_task: str
    current_project: str
    notes: str

    @classmethod
    def from_context(
        cls,
        user_id: str,
        context: UserContext,
    ) -> "ContextResponse":
        return cls(
            user_id=user_id,
            current_topic=context.current_topic,
            current_task=context.current_task,
            current_project=context.current_project,
            notes=context.notes,
        )
