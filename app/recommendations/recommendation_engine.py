from __future__ import annotations

from dataclasses import dataclass
from threading import Lock


@dataclass(frozen=True)
class Recommendation:
    title: str
    category: str
    description: str
    priority: str


class RecommendationEngine:
    def __init__(self) -> None:
        self._recommendations: dict[str, dict[str, Recommendation]] = {}
        self._lock = Lock()

    def add_recommendation(
        self,
        user_id: str,
        recommendation: Recommendation,
    ) -> Recommendation:
        with self._lock:
            user_recommendations = self._recommendations.setdefault(user_id, {})
            user_recommendations[recommendation.title.lower()] = recommendation

        return recommendation

    def get_recommendations(self, user_id: str) -> list[Recommendation]:
        with self._lock:
            return list(self._recommendations.get(user_id, {}).values())

    def get_recommendation(
        self,
        user_id: str,
        title: str,
    ) -> Recommendation | None:
        with self._lock:
            return self._recommendations.get(user_id, {}).get(title.lower())
