from __future__ import annotations

from dataclasses import dataclass
from threading import Lock


@dataclass(frozen=True)
class Project:
    name: str
    description: str
    technologies: list[str]
    progress: str


class ProjectMemoryEngine:
    def __init__(self) -> None:
        self._projects: dict[str, dict[str, Project]] = {}
        self._lock = Lock()

    def add_project(self, user_id: str, project: Project) -> Project:
        with self._lock:
            user_projects = self._projects.setdefault(user_id, {})
            user_projects[project.name.lower()] = project

        return project

    def get_projects(self, user_id: str) -> list[Project]:
        with self._lock:
            return list(self._projects.get(user_id, {}).values())

    def get_project(self, user_id: str, project_name: str) -> Project | None:
        with self._lock:
            return self._projects.get(user_id, {}).get(project_name.lower())
