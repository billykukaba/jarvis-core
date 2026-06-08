from pydantic import BaseModel, Field


class CalculationRequest(BaseModel):
    expression: str = Field(min_length=1)


class CalculationResponse(BaseModel):
    result: int | float


class TextAnalysisRequest(BaseModel):
    text: str = Field(min_length=1)


class TextAnalysisResponse(BaseModel):
    word_count: int
    character_count: int
