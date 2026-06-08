from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from threading import Lock


@dataclass(frozen=True)
class HabitRecord:
    user_id: str
    activity: str
    hour: int
    frequency_count: int


@dataclass(frozen=True)
class HabitPrediction:
    predicted_activity: str | None
    confidence: float


class HabitEngine:
    def __init__(self) -> None:
        self._habits: dict[str, dict[int, dict[str, int]]] = {}
        self._lock = Lock()

    def record_activity(self, user_id: str, activity: str) -> HabitRecord:
        hour = self._current_hour()
        normalized_activity = activity.strip().lower()

        with self._lock:
            user_habits = self._habits.setdefault(user_id, {})
            hourly_habits = user_habits.setdefault(hour, {})
            hourly_habits[normalized_activity] = hourly_habits.get(normalized_activity, 0) + 1

            return HabitRecord(
                user_id=user_id,
                activity=normalized_activity,
                hour=hour,
                frequency_count=hourly_habits[normalized_activity],
            )

    def get_habits(self, user_id: str) -> list[HabitRecord]:
        with self._lock:
            user_habits = self._habits.get(user_id, {})
            records = [
                HabitRecord(
                    user_id=user_id,
                    activity=activity,
                    hour=hour,
                    frequency_count=frequency_count,
                )
                for hour, activities in user_habits.items()
                for activity, frequency_count in activities.items()
            ]

        return sorted(records, key=lambda record: (record.hour, record.activity))

    def predict_next_activity(self, user_id: str) -> HabitPrediction:
        hour = self._current_hour()

        with self._lock:
            hourly_habits = self._habits.get(user_id, {}).get(hour, {})
            if not hourly_habits:
                return HabitPrediction(predicted_activity=None, confidence=0.0)

            predicted_activity, frequency_count = max(
                hourly_habits.items(),
                key=lambda item: item[1],
            )
            total_count = sum(hourly_habits.values())

        return HabitPrediction(
            predicted_activity=predicted_activity,
            confidence=frequency_count / total_count,
        )

    @staticmethod
    def _current_hour() -> int:
        return datetime.now(timezone.utc).hour
