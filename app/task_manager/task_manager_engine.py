from __future__ import annotations

from dataclasses import dataclass, replace
from threading import Lock


@dataclass(frozen=True)
class Task:
    title: str
    description: str
    status: str
    priority: str
    completed: bool


class TaskManagerEngine:
    def __init__(self) -> None:
        self._tasks: dict[str, dict[str, Task]] = {}
        self._lock = Lock()

    def create_task(self, user_id: str, task: Task) -> Task:
        with self._lock:
            user_tasks = self._tasks.setdefault(user_id, {})
            user_tasks[task.title.lower()] = task

        return task

    def get_tasks(self, user_id: str) -> list[Task]:
        with self._lock:
            return list(self._tasks.get(user_id, {}).values())

    def get_task(self, user_id: str, title: str) -> Task | None:
        with self._lock:
            return self._tasks.get(user_id, {}).get(title.lower())

    def update_task_status(
        self,
        user_id: str,
        title: str,
        status: str,
    ) -> Task | None:
        with self._lock:
            user_tasks = self._tasks.get(user_id)
            if user_tasks is None:
                return None

            task = user_tasks.get(title.lower())
            if task is None:
                return None

            updated_task = replace(task, status=status)
            user_tasks[title.lower()] = updated_task

        return updated_task

    def mark_completed(self, user_id: str, title: str) -> Task | None:
        with self._lock:
            user_tasks = self._tasks.get(user_id)
            if user_tasks is None:
                return None

            task = user_tasks.get(title.lower())
            if task is None:
                return None

            completed_task = replace(task, completed=True)
            user_tasks[title.lower()] = completed_task

        return completed_task

    def delete_task(self, user_id: str, title: str) -> Task | None:
        with self._lock:
            user_tasks = self._tasks.get(user_id)
            if user_tasks is None:
                return None

            return user_tasks.pop(title.lower(), None)
