from __future__ import annotations

from dataclasses import dataclass

from app.consciousness.goal_engine import GoalEngine
from app.consciousness.mood_engine import Mood, MoodEngine
from app.knowledge.knowledge_engine import KnowledgeEngine
from app.learning.learning_engine import LearningEngine
from app.profile.profile_engine import ProfileEngine


@dataclass(frozen=True)
class DecisionResult:
    decision: str
    reason: str


class DecisionEngine:
    def __init__(
        self,
        profile_engine: ProfileEngine,
        goal_engine: GoalEngine,
        knowledge_engine: KnowledgeEngine,
        learning_engine: LearningEngine,
        mood_engine: MoodEngine,
    ) -> None:
        self._profile_engine = profile_engine
        self._goal_engine = goal_engine
        self._knowledge_engine = knowledge_engine
        self._learning_engine = learning_engine
        self._mood_engine = mood_engine

    def make_decision(self, user_id: str, question: str) -> DecisionResult:
        normalized_question = question.lower()
        profile = self._profile_engine.get_profile(user_id)
        knowledge = self._knowledge_engine.get_all_knowledge(user_id)
        goals = self._goal_engine.get_goals(user_id)
        learned_skills = self._learning_engine.get_skills(user_id)
        mood = self._mood_engine.get_user_mood(user_id)

        if "python" in normalized_question and "flutter" in normalized_question:
            return self._decide_python_or_flutter(
                goals=goals,
                learned_skills=learned_skills,
                knowledge=knowledge,
                profile_skills=profile.skills,
            )

        if "mit" in normalized_question or self._has_mit_dream(profile.dream, knowledge):
            return DecisionResult(
                decision="Focus on strengthening English and Mathematics first.",
                reason=(
                    "Your profile or question points toward MIT, and English plus "
                    "Mathematics are foundational before SAT preparation, projects, "
                    "and advanced technical work."
                ),
            )

        if mood.mood == Mood.TIRED:
            return DecisionResult(
                decision="Focus on one small, manageable step first.",
                reason="Your current mood is tired, so a smaller action is more realistic.",
            )

        if "python" in normalized_question or self._has_python_goal_or_skill(
            goals=goals,
            learned_skills=learned_skills,
        ):
            return DecisionResult(
                decision="Focus on Python programming fundamentals before advanced projects.",
                reason=(
                    "Python appears in your question, goals, or learned skills, so "
                    "programming fundamentals are the strongest next step."
                ),
            )

        if goals:
            active_goals = [goal for goal in goals if not goal.completed]
            if active_goals:
                return DecisionResult(
                    decision=f"Focus on your active goal first: {active_goals[0].title}.",
                    reason="You already have an unfinished goal, so continuing it avoids spreading focus.",
                )

        if profile.dream:
            return DecisionResult(
                decision=f"Focus on the next small step toward {profile.dream}.",
                reason="Your profile contains a long-term dream, so the decision should support it.",
            )

        return DecisionResult(
            decision="Collect more profile, knowledge, goal, and skill data before deciding.",
            reason="There is not enough context yet to make a confident personalized decision.",
        )

    def _decide_python_or_flutter(
        self,
        goals: list[object],
        learned_skills: list[str],
        knowledge: dict[str, object],
        profile_skills: list[str],
    ) -> DecisionResult:
        known_skills = {skill.strip().lower() for skill in learned_skills + profile_skills}
        goal_titles = [goal.title.lower() for goal in goals]
        knowledge_values = " ".join(str(value).lower() for value in knowledge.values())

        if "flutter" in known_skills or any("flutter" in title for title in goal_titles):
            return DecisionResult(
                decision="Choose Flutter if your priority is building mobile apps now.",
                reason="Flutter already appears in your skills or goals, so it matches your current direction.",
            )

        if (
            "python" in known_skills
            or any("python" in title for title in goal_titles)
            or "ai" in knowledge_values
        ):
            return DecisionResult(
                decision="Choose Python first.",
                reason=(
                    "Your profile, goals, knowledge, or learned skills point toward "
                    "Python or AI, and Python is the stronger foundation for that path."
                ),
            )

        return DecisionResult(
            decision="Choose Python first, then learn Flutter later.",
            reason="Python builds general programming fundamentals before you specialize in app development.",
        )

    @staticmethod
    def _has_mit_dream(dream: str, knowledge: dict[str, object]) -> bool:
        values = [
            dream,
            str(knowledge.get("dream", "")),
            str(knowledge.get("dream_university", "")),
        ]
        return any(value.strip().lower() == "mit" for value in values)

    @staticmethod
    def _has_python_goal_or_skill(
        goals: list[object],
        learned_skills: list[str],
    ) -> bool:
        return any("python" in goal.title.lower() for goal in goals) or any(
            skill.strip().lower() == "python" for skill in learned_skills
        )
