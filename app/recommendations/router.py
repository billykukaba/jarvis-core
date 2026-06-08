from fastapi import APIRouter, HTTPException, status

from app.recommendations.schemas import (
    RecommendationRequest,
    RecommendationResponse,
    UserRecommendationsResponse,
)
from app.services.engine_registry import recommendation_engine

router = APIRouter(tags=["recommendations"])


@router.post("/recommendations/{user_id}", response_model=RecommendationResponse)
async def add_recommendation(
    user_id: str,
    request: RecommendationRequest,
) -> RecommendationResponse:
    recommendation = recommendation_engine.add_recommendation(
        user_id,
        request.to_recommendation(),
    )
    return RecommendationResponse.from_recommendation(recommendation)


@router.get(
    "/recommendations/{user_id}",
    response_model=UserRecommendationsResponse,
)
async def get_recommendations(user_id: str) -> UserRecommendationsResponse:
    recommendations = recommendation_engine.get_recommendations(user_id)
    return UserRecommendationsResponse(
        user_id=user_id,
        recommendations=[
            RecommendationResponse.from_recommendation(recommendation)
            for recommendation in recommendations
        ],
    )


@router.get(
    "/recommendations/{user_id}/{title}",
    response_model=RecommendationResponse,
)
async def get_recommendation(user_id: str, title: str) -> RecommendationResponse:
    recommendation = recommendation_engine.get_recommendation(user_id, title)
    if recommendation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recommendation not found",
        )

    return RecommendationResponse.from_recommendation(recommendation)
