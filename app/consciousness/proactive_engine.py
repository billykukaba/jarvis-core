from __future__ import annotations

from dataclasses import dataclass
import logging
from typing import Any

from app.consciousness.goal_engine import GoalEngine, GoalRecord
from app.consciousness.habit_engine import HabitEngine, HabitPrediction
from app.consciousness.mood_engine import Mood, MoodEngine, MoodRecord
from app.memory.memory_engine import MemoryEngine

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ProactiveAnalysis:
    user_id: str
    habit_prediction: HabitPrediction
    favorite_music: Any
    mood: MoodRecord
    active_goals: list[GoalRecord]
    completed_goals: list[GoalRecord]


class ProactiveEngine:
    def __init__(
        self,
        habit_engine: HabitEngine,
        memory_engine: MemoryEngine,
        mood_engine: MoodEngine,
        goal_engine: GoalEngine,
    ) -> None:
        self._habit_engine = habit_engine
        self._memory_engine = memory_engine
        self._mood_engine = mood_engine
        self._goal_engine = goal_engine

    def analyze_user(self, user_id: str) -> ProactiveAnalysis:
        favorite_music = self._memory_engine.recall(user_id, "favorite_music")
        goals = self._goal_engine.get_goals(user_id)
        habit_prediction = self._habit_engine.predict_next_activity(user_id)
        mood = self._mood_engine.get_user_mood(user_id)
        active_goals = [goal for goal in goals if not goal.completed]
        completed_goals = [goal for goal in goals if goal.completed]

        logger.debug(
            "Proactive analysis for user_id=%s favorite_music=%r mood=%s "
            "active_goals=%s completed_goals=%s habit_prediction=%r",
            user_id,
            favorite_music.value if favorite_music else None,
            mood.mood.value,
            [goal.title for goal in active_goals],
            [goal.title for goal in completed_goals],
            habit_prediction.predicted_activity,
        )

        return ProactiveAnalysis(
            user_id=user_id,
            habit_prediction=habit_prediction,
            favorite_music=favorite_music.value if favorite_music else None,
            mood=mood,
            active_goals=active_goals,
            completed_goals=completed_goals,
        )

    def generate_suggestion(self, user_id: str) -> list[str]:
        analysis = self.analyze_user(user_id)
        suggestions: list[str] = []

        if analysis.habit_prediction.predicted_activity:
            suggestions.append(
                f"Based on your habits, would you like to {analysis.habit_prediction.predicted_activity}?"
            )

        if analysis.favorite_music:
            suggestions.append(f"Would you like to listen to {analysis.favorite_music}?")

        if analysis.mood.mood == Mood.HAPPY:
            suggestions.append("You seem happy today.")

        for goal in analysis.completed_goals:
            suggestions.append(f"Congratulations on completing {goal.title}.")

        if analysis.active_goals:
            suggestions.append("Would you like to continue your goal?")

        logger.debug(
            "Generated proactive suggestions for user_id=%s suggestions=%s",
            user_id,
            suggestions,
        )
        return suggestions
