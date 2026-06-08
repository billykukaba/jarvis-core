"""Task engine with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.tasks.schemas import Task

# In-memory task store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "title": "Practice English",
#             "description": "Study American English for 2 hours",
#             "status": "pending",
#         }
#     ]
# }
tasks_db: dict[str, list[Task]] = {}


class TaskEngine:
    """Manage user tasks stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def create_task(self, user_id: str, task: Task) -> Task:
        """Create and store a task for the given user."""
        with self._lock:
            user_tasks = tasks_db.setdefault(user_id, [])
            user_tasks.append(task)

        return task

    def get_tasks(self, user_id: str) -> list[Task]:
        """Return all tasks for the given user."""
        with self._lock:
            return list(tasks_db.get(user_id, []))

    def get_task(self, user_id: str, title: str) -> Task | None:
        """Return one task by title for the given user."""
        with self._lock:
            return self._find_task(user_id, title)

    def update_task(self, user_id: str, title: str, task: Task) -> Task | None:
        """Replace an existing task with a new version."""
        with self._lock:
            user_tasks = tasks_db.get(user_id)
            if user_tasks is None:
                return None

            index = self._find_task_index(user_tasks, title)
            if index is None:
                return None

            user_tasks[index] = task

        return task

    def delete_task(self, user_id: str, title: str) -> Task | None:
        """Delete and return a task by title."""
        with self._lock:
            user_tasks = tasks_db.get(user_id)
            if user_tasks is None:
                return None

            index = self._find_task_index(user_tasks, title)
            if index is None:
                return None

            return user_tasks.pop(index)

    def _find_task(self, user_id: str, title: str) -> Task | None:
        """Locate a task in the user's list by title."""
        user_tasks = tasks_db.get(user_id, [])
        index = self._find_task_index(user_tasks, title)
        if index is None:
            return None
        return user_tasks[index]

    @staticmethod
    def _find_task_index(user_tasks: list[Task], title: str) -> int | None:
        """Return the list index for a task title, if it exists."""
        normalized_title = title.lower()
        for index, task in enumerate(user_tasks):
            if task.title.lower() == normalized_title:
                return index
        return None
