from __future__ import annotations

from dataclasses import dataclass, field
from threading import Lock
from typing import Any

from app.chat.conversation_history import ConversationHistory
from app.consciousness.goal_engine import GoalEngine
from app.knowledge.knowledge_engine import KnowledgeEngine
from app.memory.memory_engine import MemoryEngine


@dataclass(frozen=True)
class UserProfile:
    dream: str = ""
    skills: list[str] = field(default_factory=list)
    interests: list[str] = field(default_factory=list)
    projects: list[str] = field(default_factory=list)


class ProfileEngine:
    def __init__(
        self,
        memory_engine: MemoryEngine,
        knowledge_engine: KnowledgeEngine,
        goal_engine: GoalEngine,
        conversation_history: ConversationHistory,
    ) -> None:
        self._memory_engine = memory_engine
        self._knowledge_engine = knowledge_engine
        self._goal_engine = goal_engine
        self._conversation_history = conversation_history
        self._profiles: dict[str, UserProfile] = {}
        self._lock = Lock()

    def build_profile(self, user_id: str) -> UserProfile:
        memories = self._memory_engine.get_all_memories(user_id)
        knowledge = self._knowledge_engine.get_all_knowledge(user_id)
        goals = self._goal_engine.get_goals(user_id)
        messages = self._conversation_history.get_messages(user_id)

        profile = UserProfile(
            dream=self._extract_dream(memories, knowledge),
            skills=self._extract_skills(memories, knowledge, messages),
            interests=self._extract_interests(memories, knowledge, messages),
            projects=self._extract_projects(memories, knowledge, goals, messages),
        )

        with self._lock:
            self._profiles[user_id] = profile

        return profile

    def get_profile(self, user_id: str) -> UserProfile:
        with self._lock:
            profile = self._profiles.get(user_id)

        if profile is not None:
            return profile

        return self.build_profile(user_id)

    @staticmethod
    def _extract_dream(memories: dict[str, Any], knowledge: dict[str, Any]) -> str:
        for key in ("dream", "dream_university", "goal", "field"):
            value = knowledge.get(key) or memories.get(key)
            if value:
                return str(value)

        return ""

    @classmethod
    def _extract_skills(
        cls,
        memories: dict[str, Any],
        knowledge: dict[str, Any],
        messages: list[Any],
    ) -> list[str]:
        values = cls._collect_values(
            memories=memories,
            knowledge=knowledge,
            topics=("skill", "skills", "language", "languages", "field"),
        )
        values.extend(cls._extract_keywords(messages, {"python", "ai", "fastapi"}))
        return cls._unique(values)

    @classmethod
    def _extract_interests(
        cls,
        memories: dict[str, Any],
        knowledge: dict[str, Any],
        messages: list[Any],
    ) -> list[str]:
        values = cls._collect_values(
            memories=memories,
            knowledge=knowledge,
            topics=("interest", "interests", "favorite_music", "field"),
        )
        values.extend(cls._extract_keywords(messages, {"music", "ai", "gospel"}))
        return cls._unique(values)

    @classmethod
    def _extract_projects(
        cls,
        memories: dict[str, Any],
        knowledge: dict[str, Any],
        goals: list[Any],
        messages: list[Any],
    ) -> list[str]:
        values = cls._collect_values(
            memories=memories,
            knowledge=knowledge,
            topics=("project", "projects", "app"),
        )
        values.extend(goal.title for goal in goals)
        values.extend(cls._extract_keywords(messages, {"jarvis"}))
        return cls._unique(values)

    @staticmethod
    def _collect_values(
        memories: dict[str, Any],
        knowledge: dict[str, Any],
        topics: tuple[str, ...],
    ) -> list[str]:
        values: list[str] = []
        for topic in topics:
            for source in (knowledge, memories):
                value = source.get(topic)
                if isinstance(value, list):
                    values.extend(str(item) for item in value if item)
                elif value:
                    values.append(str(value))

        return values

    @staticmethod
    def _extract_keywords(messages: list[Any], keywords: set[str]) -> list[str]:
        found: list[str] = []
        for message in messages:
            content = message.content.lower()
            for keyword in keywords:
                if keyword in content:
                    found.append(keyword.upper() if keyword == "ai" else keyword.title())

        return found

    @staticmethod
    def _unique(values: list[str]) -> list[str]:
        unique_values: list[str] = []
        seen: set[str] = set()

        for value in values:
            normalized_value = value.strip()
            lookup_value = normalized_value.lower()
            if normalized_value and lookup_value not in seen:
                unique_values.append(normalized_value)
                seen.add(lookup_value)

        return unique_values
