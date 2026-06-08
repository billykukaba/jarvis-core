"""Projects Service engine with thread-safe in-memory storage."""

from __future__ import annotations

from threading import Lock

from app.projects.schemas import Project

# In-memory project store keyed by user_id.
# Example:
# {
#     "billy": [
#         {
#             "name": "AI Social Network",
#             "description": "AI powered social platform",
#             "year": 2032,
#         }
#     ]
# }
projects_db: dict[str, list[Project]] = {}


class ProjectServiceEngine:
    """Manage user project records stored in memory."""

    def __init__(self) -> None:
        self._lock = Lock()

    def name_exists(self, user_id: str, name: str) -> bool:
        """Return True if a project with this name already exists."""
        with self._lock:
            return self._find_project_index(projects_db.get(user_id, []), name) is not None

    def create_project(self, user_id: str, project: Project) -> Project:
        """Create and store a project for the given user."""
        with self._lock:
            user_projects = projects_db.setdefault(user_id, [])
            user_projects.append(project)

        return project

    def get_projects(self, user_id: str) -> list[Project]:
        """Return all projects for the given user."""
        with self._lock:
            return list(projects_db.get(user_id, []))

    def get_project(self, user_id: str, name: str) -> Project | None:
        """Return one project by name for the given user."""
        with self._lock:
            return self._find_project(user_id, name)

    def update_project(
        self,
        user_id: str,
        name: str,
        project: Project,
    ) -> Project | None:
        """Replace an existing project with a new version."""
        with self._lock:
            user_projects = projects_db.get(user_id)
            if user_projects is None:
                return None

            index = self._find_project_index(user_projects, name)
            if index is None:
                return None

            user_projects[index] = project

        return project

    def delete_project(self, user_id: str, name: str) -> Project | None:
        """Delete and return a project by name."""
        with self._lock:
            user_projects = projects_db.get(user_id)
            if user_projects is None:
                return None

            index = self._find_project_index(user_projects, name)
            if index is None:
                return None

            return user_projects.pop(index)

    def _find_project(self, user_id: str, name: str) -> Project | None:
        """Locate a project in the user's list by name."""
        user_projects = projects_db.get(user_id, [])
        index = self._find_project_index(user_projects, name)
        if index is None:
            return None
        return user_projects[index]

    @staticmethod
    def _find_project_index(user_projects: list[Project], name: str) -> int | None:
        """Return the list index for a project name, if it exists."""
        normalized_name = name.lower()
        for index, project in enumerate(user_projects):
            if project.name.lower() == normalized_name:
                return index
        return None
