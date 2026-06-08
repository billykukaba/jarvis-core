from typing import TYPE_CHECKING

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from app.websearch.websearch_engine import SearchResult


class WebSearchRequest(BaseModel):
    query: str = Field(min_length=1)


class WebSearchResultResponse(BaseModel):
    title: str
    url: str
    snippet: str

    @classmethod
    def from_result(cls, result: "SearchResult") -> "WebSearchResultResponse":
        return cls(
            title=result.title,
            url=result.url,
            snippet=result.snippet,
        )


class WebSearchResponse(BaseModel):
    query: str
    results: list[WebSearchResultResponse]
