from pydantic import BaseModel


class ProactiveResponse(BaseModel):
    user_id: str
    suggestions: list[str]
