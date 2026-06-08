from __future__ import annotations

from app.consciousness.goal_engine import GoalEngine
from app.knowledge.knowledge_engine import KnowledgeEngine
from app.profile.profile_engine import ProfileEngine


class ReasoningEngine:
    def __init__(
        self,
        profile_engine: ProfileEngine,
        knowledge_engine: KnowledgeEngine,
        goal_engine: GoalEngine,
    ) -> None:
        self._profile_engine = profile_engine
        self._knowledge_engine = knowledge_engine
        self._goal_engine = goal_engine

    def answer_question(self, user_id: str, question: str) -> str:
        profile = self._profile_engine.get_profile(user_id)
        knowledge = self._knowledge_engine.get_all_knowledge(user_id)
        goals = self._goal_engine.get_goals(user_id)
        suggestions: list[str] = []

        if self._is_mit_dream(profile.dream, knowledge):
            suggestions.extend(
                [
                    "strengthen your English",
                    "build a strong Mathematics foundation",
                    "continue learning Python",
                    "create serious projects",
                    "prepare for the SAT",
                ]
            )

        if any("python" in goal.title.lower() for goal in goals):
            suggestions.append("learn programming fundamentals")

        if not suggestions:
            return self._fallback_answer(question)

        return self._format_answer(question, suggestions)

    @staticmethod
    def _is_mit_dream(dream: str, knowledge: dict[str, object]) -> bool:
        dream_values = [
            dream,
            str(knowledge.get("dream", "")),
            str(knowledge.get("dream_university", "")),
        ]
        return any(value.strip().lower() == "mit" for value in dream_values)

    @staticmethod
    def _format_answer(question: str, suggestions: list[str]) -> str:
        unique_suggestions = list(dict.fromkeys(suggestions))
        plan = ", ".join(unique_suggestions[:-1])
        if len(unique_suggestions) > 1:
            plan = f"{plan}, and {unique_suggestions[-1]}"
        else:
            plan = unique_suggestions[0]

        return f"For your question '{question}', I recommend you {plan}."

    @staticmethod
    def _fallback_answer(question: str) -> str:
        return (
            f"For your question '{question}', I need more profile, knowledge, "
            "or goal data before I can give a focused plan."
        )
