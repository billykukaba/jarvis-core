from __future__ import annotations

from dataclasses import dataclass
from threading import Lock


@dataclass(frozen=True)
class PersonalityProfile:
    name: str
    tone: str
    communication_style: str
    language: str
    traits: list[str]


class PersonalityEngine:
    def __init__(self) -> None:
        self._profiles: dict[str, PersonalityProfile] = {}
        self._lock = Lock()

    def create_profile(
        self,
        user_id: str,
        profile: PersonalityProfile,
    ) -> PersonalityProfile:
        with self._lock:
            self._profiles[user_id] = profile

        return profile

    def get_profile(self, user_id: str) -> PersonalityProfile | None:
        with self._lock:
            return self._profiles.get(user_id)

    def update_profile(
        self,
        user_id: str,
        profile: PersonalityProfile,
    ) -> PersonalityProfile:
        return self.create_profile(user_id, profile)
