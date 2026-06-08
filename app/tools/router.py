from fastapi import APIRouter, HTTPException, status

from app.services.engine_registry import tool_engine
from app.tools.schemas import (
    CalculationRequest,
    CalculationResponse,
    TextAnalysisRequest,
    TextAnalysisResponse,
)

router = APIRouter(tags=["tools"])


@router.post("/tools/calculate", response_model=CalculationResponse)
async def calculate(request: CalculationRequest) -> CalculationResponse:
    try:
        result = tool_engine.calculate(request.expression)
    except (SyntaxError, ValueError, ZeroDivisionError) as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error

    return CalculationResponse(result=result)


@router.post("/tools/analyze", response_model=TextAnalysisResponse)
async def analyze_text(request: TextAnalysisRequest) -> TextAnalysisResponse:
    analysis = tool_engine.analyze_text(request.text)
    return TextAnalysisResponse(
        word_count=analysis.word_count,
        character_count=analysis.character_count,
    )
