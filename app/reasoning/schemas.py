from pydantic import BaseModel, Field


class ReasoningRequest(BaseModel):
    question: str = Field(min_length=1)


class ReasoningResponse(BaseModel):
    answer: str
