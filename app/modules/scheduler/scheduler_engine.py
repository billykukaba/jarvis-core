from __future__ import annotations

from threading import Lock

from app.modules.scheduler.schemas import Schedule

schedules_db: dict[str, dict[str, Schedule]] = {}


class SchedulerEngine:
    def __init__(self) -> None:
        self._lock = Lock()

    def create_schedule(self, user_id: str, schedule: Schedule) -> Schedule:
        with self._lock:
            user_schedules = schedules_db.setdefault(user_id, {})
            user_schedules[schedule.task_title.lower()] = schedule

        return schedule

    def get_schedules(self, user_id: str) -> list[Schedule]:
        with self._lock:
            return list(schedules_db.get(user_id, {}).values())

    def get_schedule(self, user_id: str, task_title: str) -> Schedule | None:
        with self._lock:
            return schedules_db.get(user_id, {}).get(task_title.lower())

    def update_schedule(
        self,
        user_id: str,
        task_title: str,
        schedule: Schedule,
    ) -> Schedule | None:
        with self._lock:
            user_schedules = schedules_db.get(user_id)
            if user_schedules is None or task_title.lower() not in user_schedules:
                return None

            user_schedules[task_title.lower()] = schedule

        return schedule

    def delete_schedule(self, user_id: str, task_title: str) -> Schedule | None:
        with self._lock:
            user_schedules = schedules_db.get(user_id)
            if user_schedules is None:
                return None

            return user_schedules.pop(task_title.lower(), None)
