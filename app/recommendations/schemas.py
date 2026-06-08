from pydantic import BaseModel, Field

from app.recommendations.recommendation_engine import Recommendation


class RecommendationRequest(BaseModel):
    title: str = Field(min_length=1)
    category: str = Field(min_length=1)
    description: str = Field(min_length=1)
    priority: str = Field(min_length=1)

    def to_recommendation(self) -> Recommendation:
        return Recommendation(
            title=self.title,
            category=self.category,
            description=self.description,
            priority=self.priority,
        )


class RecommendationResponse(BaseModel):
    title: str
    category: str
    description: str
    priority: str

    @classmethod
    def from_recommendation(
        cls,
        recommendation: Recommendation,
    ) -> "RecommendationResponse":
        return cls(
            title=recommendation.title,
            category=recommendation.category,
            description=recommendation.description,
            priority=recommendation.priority,
        )


class UserRecommendationsResponse(BaseModel):
    user_id: str
    recommendations: list[RecommendationResponse]
