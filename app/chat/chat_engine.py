from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from app.consciousness.goal_engine import GoalEngine, GoalRecord
from app.consciousness.habit_engine import HabitEngine, HabitPrediction
from app.consciousness.mood_engine import Mood, MoodEngine, MoodRecord
from app.memory.memory_engine import MemoryEngine
from app.chat.conversation_history import ConversationHistory, ConversationMessage


@dataclass(frozen=True)
class ChatContext:
    user_id: str
    memories: dict[str, Any]
    mood: MoodRecord
    goals: list[GoalRecord]
    habit_prediction: HabitPrediction
    conversation_history: list[ConversationMessage]


class ChatEngine:
    def __init__(
        self,
        memory_engine: MemoryEngine,
        mood_engine: MoodEngine,
        goal_engine: GoalEngine,
        habit_engine: HabitEngine,
        conversation_history: ConversationHistory,
    ) -> None:
        self._memory_engine = memory_engine
        self._mood_engine = mood_engine
        self._goal_engine = goal_engine
        self._habit_engine = habit_engine
        self._conversation_history = conversation_history

    def build_context_summary(self, user_id: str) -> ChatContext:
        return ChatContext(
            user_id=user_id,
            memories=self._memory_engine.get_all_memories(user_id),
            mood=self._mood_engine.get_user_mood(user_id),
            goals=self._goal_engine.get_goals(user_id),
            habit_prediction=self._habit_engine.predict_next_activity(user_id),
            conversation_history=self._conversation_history.get_messages(user_id),
        )

    def generate_reply(self, user_id: str, message: str) -> str:
        context = self.build_context_summary(user_id)
        name = self._display_name(user_id)
        reply_parts = [self._greeting(name, message)]

        mood_reply = self._mood_reply(context.mood)
        if mood_reply:
            reply_parts.append(mood_reply)

        favorite_music = context.memories.get("favorite_music")
        if favorite_music:
            reply_parts.append(f"I remember you like {favorite_music} music.")

        active_goals = [goal for goal in context.goals if not goal.completed]
        completed_goals = [goal for goal in context.goals if goal.completed]

        if active_goals:
            reply_parts.append(f"How is your {active_goals[0].title} goal progressing?")
        elif completed_goals:
            reply_parts.append(f"Congratulations again on completing {completed_goals[0].title}.")

        if context.habit_prediction.predicted_activity:
            reply_parts.append(
                f"It may also be a good time for {context.habit_prediction.predicted_activity}."
            )

        history_reply = self._history_reply(context.conversation_history)
        if history_reply:
            reply_parts.append(history_reply)

        if len(reply_parts) == 1:
            reply_parts.append("How can I help you today?")

        reply = " ".join(reply_parts)
        self._conversation_history.add_message(user_id, "user", message)
        self._conversation_history.add_message(user_id, "jarvis", reply)

        return reply

    def get_history(self, user_id: str) -> list[ConversationMessage]:
        return self._conversation_history.get_messages(user_id)

    @staticmethod
    def _display_name(user_id: str) -> str:
        return user_id.replace("_", " ").replace("-", " ").title()

    @staticmethod
    def _greeting(name: str, message: str) -> str:
        normalized_message = message.strip().lower()
        if normalized_message.startswith(("hello", "hi", "hey")):
            return f"Hello {name}."

        return f"{name}, I hear you."

    @staticmethod
    def _mood_reply(mood: MoodRecord) -> str | None:
        if mood.mood == Mood.HAPPY:
            return "You seem happy today."
        if mood.mood == Mood.EXCITED:
            return "You sound excited."
        if mood.mood == Mood.SAD:
            return "I can tell this may be a difficult moment."
        if mood.mood == Mood.TIRED:
            return "You seem tired, so we can keep things simple."

        return None

    @staticmethod
    def _history_reply(history: list[ConversationMessage]) -> str | None:
        previous_user_messages = [
            message.content for message in history if message.role == "user"
        ]
        if not previous_user_messages:
            return None

        return f"Last time, you said: {previous_user_messages[-1]}"
