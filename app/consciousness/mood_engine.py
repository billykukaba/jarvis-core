from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from threading import Lock


class Mood(str, Enum):
    HAPPY = "HAPPY"
    NEUTRAL = "NEUTRAL"
    SAD = "SAD"
    EXCITED = "EXCITED"
    TIRED = "TIRED"


@dataclass(frozen=True)
class MoodRecord:
    user_id: str
    mood: Mood


class MoodEngine:
    _keywords: dict[Mood, set[str]] = {
        Mood.HAPPY: {"happy", "joy", "great", "good", "smile", "grateful"},
        Mood.SAD: {"sad", "down", "upset", "cry", "lonely", "depressed"},
        Mood.EXCITED: {"excited", "amazing", "awesome", "thrilled", "pumped"},
        Mood.TIRED: {"tired", "sleepy", "exhausted", "drained", "fatigued"},
    }

    def __init__(self) -> None:
        self._user_moods: dict[str, Mood] = {}
        self._lock = Lock()

    def analyze_mood(self, text: str) -> Mood:
        normalized_text = text.lower()
        scores = {
            mood: sum(keyword in normalized_text for keyword in keywords)
            for mood, keywords in self._keywords.items()
        }
        strongest_mood, strongest_score = max(scores.items(), key=lambda item: item[1])

        if strongest_score == 0:
            return Mood.NEUTRAL

        return strongest_mood

    def get_user_mood(self, user_id: str) -> MoodRecord:
        with self._lock:
            mood = self._user_moods.get(user_id, Mood.NEUTRAL)

        return MoodRecord(user_id=user_id, mood=mood)

    def update_user_mood(self, user_id: str, text: str) -> MoodRecord:
        mood = self.analyze_mood(text)

        with self._lock:
            self._user_moods[user_id] = mood

        return MoodRecord(user_id=user_id, mood=mood)
