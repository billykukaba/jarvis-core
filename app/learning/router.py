from fastapi import APIRouter

from app.learning.schemas import LearningRequest, LearningResponse, UserSkillsResponse
from app.services.engine_registry import learning_engine

router = APIRouter(tags=["learning"])


@router.post("/learning/{user_id}", response_model=LearningResponse)
async def learn_skill(user_id: str, request: LearningRequest) -> LearningResponse:
    learned_skill = learning_engine.learn_skill(user_id, request.skill)
    return LearningResponse.from_skill(learned_skill)


@router.get("/learning/{user_id}", response_model=UserSkillsResponse)
async def get_skills(user_id: str) -> UserSkillsResponse:
    skills = learning_engine.get_skills(user_id)
    return UserSkillsResponse(user_id=user_id, skills=skills)
