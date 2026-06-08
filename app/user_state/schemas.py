from pydantic import BaseModel, Field

from app.user_state.user_state_engine import UserState


class UserStateRequest(BaseModel):
    level: str = Field(min_length=1)
    target: str = Field(min_length=1)
    current_focus: str = Field(min_length=1)
    current_project: str = Field(min_length=1)
    status: str = Field(min_length=1)

    def to_state(self) -> UserState:
        return UserState(
            level=self.level,
            target=self.target,
            current_focus=self.current_focus,
            current_project=self.current_project,
            status=self.status,
        )


class UserStateResponse(BaseModel):
    user_id: str
    level: str
    target: str
    current_focus: str
    current_project: str
    status: str

    @classmethod
    def from_state(cls, user_id: str, state: UserState) -> "UserStateResponse":
        return cls(
            user_id=user_id,
            level=state.level,
            target=state.target,
            current_focus=state.current_focus,
            current_project=state.current_project,
            status=state.status,
        )
