import logging

from fastapi import APIRouter

from app.services.engine_registry import websearch_engine
from app.websearch.schemas import (
    WebSearchRequest,
    WebSearchResponse,
    WebSearchResultResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter(tags=["websearch"])


@router.post("/websearch/search", response_model=WebSearchResponse)
async def search_web(request: WebSearchRequest) -> WebSearchResponse:
    print("ROUTER CALLED")
    logger.info("Web search route called query=%r", request.query)
    results = websearch_engine.search(request.query)
    logger.info(
        "Web search route returning query=%r result_count=%s",
        request.query,
        len(results),
    )

    return WebSearchResponse(
        query=request.query,
        results=[
            WebSearchResultResponse.from_result(result)
            for result in results
        ],
    )
