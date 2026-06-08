from __future__ import annotations

from dataclasses import dataclass
import json
from json import JSONDecodeError
import logging
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class SearchResult:
    title: str
    url: str
    snippet: str


class WebSearchEngine:
    def __init__(self, max_results: int = 5, timeout_seconds: int = 10) -> None:
        self._max_results = max_results
        self._timeout_seconds = timeout_seconds
        self._base_url = "https://api.duckduckgo.com/"

    def search(self, query: str) -> list[SearchResult]:
        print("WEBSEARCH CALLED")
        target_url = self._build_request_url(query)
        request = Request(
            url=target_url,
            headers={
                "Accept": "application/json",
                "User-Agent": "JARVIS_CORE/0.1",
            },
        )

        logger.info("Web search started query=%r", query)
        logger.info("Web search request URL=%s", target_url)

        try:
            with urlopen(request, timeout=self._timeout_seconds) as response:
                status_code = getattr(response, "status", None)
                logger.info("Web search response status=%s", status_code)
                payload = json.loads(response.read().decode("utf-8"))
                print("PAYLOAD KEYS:", payload.keys())
                print("ABSTRACT:", payload.get("AbstractText"))
                print("RESULTS COUNT:", len(payload.get("Results", [])))
                print("RELATED COUNT:", len(payload.get("RelatedTopics", [])))
        except HTTPError as error:
            logger.exception(
                "Web search HTTPError query=%r url=%s status=%s reason=%s",
                query,
                target_url,
                error.code,
                error.reason,
            )
            return []
        except URLError as error:
            logger.exception(
                "Web search URLError query=%r url=%s reason=%s",
                query,
                target_url,
                error.reason,
            )
            return []
        except TimeoutError as error:
            logger.exception(
                "Web search TimeoutError query=%r url=%s message=%s",
                query,
                target_url,
                error,
            )
            return []
        except JSONDecodeError as error:
            logger.exception(
                "Web search JSONDecodeError query=%r url=%s message=%s",
                query,
                target_url,
                error,
            )
            return []
        except Exception as error:
            logger.exception(
                "Web search unexpected exception query=%r url=%s message=%s",
                query,
                target_url,
                error,
            )
            return []

        results = self._parse_results(payload)
        logger.info("Web search results found count=%s query=%r", len(results), query)
        return results

    def _build_request_url(self, query: str) -> str:
        parameters = urlencode(
            {
                "q": query,
                "format": "json",
                "no_html": "1",
                "skip_disambig": "1",
            }
        )
        return f"{self._base_url}?{parameters}"

    def _parse_results(self, payload: dict[str, Any]) -> list[SearchResult]:
        results: list[SearchResult] = []

        abstract_url = payload.get("AbstractURL")
        abstract_text = payload.get("AbstractText")
        heading = payload.get("Heading")
        if abstract_url and (abstract_text or heading):
            results.append(
                SearchResult(
                    title=str(heading or abstract_url),
                    url=str(abstract_url),
                    snippet=str(abstract_text or ""),
                )
            )

        self._collect_results(payload.get("Results", []), results)
        self._collect_related_topics(payload.get("RelatedTopics", []), results)
        return results[: self._max_results]

    def _collect_results(
        self,
        items: list[dict[str, Any]],
        results: list[SearchResult],
    ) -> None:
        for item in items:
            if len(results) >= self._max_results:
                return

            first_url = item.get("FirstURL")
            text = item.get("Text")
            if not first_url or not text:
                continue

            title = str(text).split(" - ", maxsplit=1)[0]
            results.append(
                SearchResult(
                    title=title,
                    url=str(first_url),
                    snippet=str(text),
                )
            )

    def _collect_related_topics(
        self,
        topics: list[dict[str, Any]],
        results: list[SearchResult],
    ) -> None:
        for topic in topics:
            if len(results) >= self._max_results:
                return

            nested_topics = topic.get("Topics")
            if isinstance(nested_topics, list):
                self._collect_related_topics(nested_topics, results)
                continue

            first_url = topic.get("FirstURL")
            text = topic.get("Text")
            if not first_url or not text:
                continue

            title = str(text).split(" - ", maxsplit=1)[0]
            results.append(
                SearchResult(
                    title=title,
                    url=str(first_url),
                    snippet=str(text),
                )
            )
