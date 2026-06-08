from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from app.consciousness.goal_engine import GoalEngine
from app.consciousness.mood_engine import MoodEngine
from app.decision.decision_engine import DecisionEngine
from app.knowledge.knowledge_engine import KnowledgeEngine
from app.learning.learning_engine import LearningEngine
from app.memory.memory_engine import MemoryEngine
from app.planning.planning_engine import PlanningEngine
from app.profile.profile_engine import ProfileEngine, UserProfile
from app.reasoning.reasoning_engine import ReasoningEngine
from app.websearch.websearch_engine import WebSearchEngine


@dataclass(frozen=True)
class BrainResult:
    profile: UserProfile
    reasoning: str
    decision: str
    plan: list[str]
    recommended_skills: list[str]


class BrainEngine:
    def __init__(
        self,
        memory_engine: MemoryEngine,
        knowledge_engine: KnowledgeEngine,
        learning_engine: LearningEngine,
        goal_engine: GoalEngine,
        mood_engine: MoodEngine,
        profile_engine: ProfileEngine,
        reasoning_engine: ReasoningEngine,
        planning_engine: PlanningEngine,
        decision_engine: DecisionEngine,
        websearch_engine: WebSearchEngine,
    ) -> None:
        self._memory_engine = memory_engine
        self._knowledge_engine = knowledge_engine
        self._learning_engine = learning_engine
        self._goal_engine = goal_engine
        self._mood_engine = mood_engine
        self._profile_engine = profile_engine
        self._reasoning_engine = reasoning_engine
        self._planning_engine = planning_engine
        self._decision_engine = decision_engine
        self._websearch_engine = websearch_engine

    def process_message(self, user_id: str, message: str) -> BrainResult:
        profile = self._profile_engine.build_profile(user_id)
        reasoning = self._reasoning_engine.answer_question(user_id, message)
        decision = self._decision_engine.make_decision(user_id, message)
        plan = self._planning_engine.create_plan(user_id, message)
        web_results = self._websearch_engine.search(message)

        return BrainResult(
            profile=profile,
            reasoning=reasoning,
            decision=decision.decision,
            plan=plan,
            recommended_skills=self._recommend_skills(
                user_id=user_id,
                message=message,
                profile=profile,
                web_results=web_results,
            ),
        )

    def _recommend_skills(
        self,
        user_id: str,
        message: str,
        profile: UserProfile,
        web_results: list[Any],
    ) -> list[str]:
        context = self._build_context(user_id, message, profile, web_results)
        recommendations: list[str] = []

        if "mit" in context:
            recommendations.extend(["English", "Mathematics", "SAT preparation"])

        if "ai" in context or "engineer" in context:
            recommendations.extend(["Python", "Machine Learning", "Projects"])

        if "python" in context:
            recommendations.append("Programming fundamentals")

        return self._unique(recommendations)

    def _build_context(
        self,
        user_id: str,
        message: str,
        profile: UserProfile,
        web_results: list[Any],
    ) -> str:
        memories = self._memory_engine.get_all_memories(user_id)
        knowledge = self._knowledge_engine.get_all_knowledge(user_id)
        learned_skills = self._learning_engine.get_skills(user_id)
        goals = self._goal_engine.get_goals(user_id)
        mood = self._mood_engine.get_user_mood(user_id)

        values: list[Any] = [
            message,
            profile.dream,
            *profile.skills,
            *profile.interests,
            *profile.projects,
            *memories.values(),
            *knowledge.values(),
            *learned_skills,
            *(goal.title for goal in goals),
            mood.mood.value,
            *(result.title for result in web_results),
            *(result.snippet for result in web_results),
        ]
        return " ".join(str(value).lower() for value in values if value)

    @staticmethod
    def _unique(values: list[str]) -> list[str]:
        unique_values: list[str] = []
        seen: set[str] = set()

        for value in values:
            lookup_value = value.lower()
            if lookup_value not in seen:
                unique_values.append(value)
                seen.add(lookup_value)

        return unique_values
