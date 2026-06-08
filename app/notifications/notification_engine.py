from __future__ import annotations

from dataclasses import dataclass, replace
from threading import Lock


@dataclass(frozen=True)
class Notification:
    title: str
    message: str
    read: bool


class NotificationEngine:
    def __init__(self) -> None:
        self._notifications: dict[str, dict[str, Notification]] = {}
        self._lock = Lock()

    def create_notification(
        self,
        user_id: str,
        notification: Notification,
    ) -> Notification:
        with self._lock:
            user_notifications = self._notifications.setdefault(user_id, {})
            user_notifications[notification.title.lower()] = notification

        return notification

    def get_notifications(self, user_id: str) -> list[Notification]:
        with self._lock:
            return list(self._notifications.get(user_id, {}).values())

    def get_notification(self, user_id: str, title: str) -> Notification | None:
        with self._lock:
            return self._notifications.get(user_id, {}).get(title.lower())

    def mark_read(self, user_id: str, title: str) -> Notification | None:
        with self._lock:
            user_notifications = self._notifications.get(user_id)
            if user_notifications is None:
                return None

            notification = user_notifications.get(title.lower())
            if notification is None:
                return None

            read_notification = replace(notification, read=True)
            user_notifications[title.lower()] = read_notification

        return read_notification

    def delete_notification(self, user_id: str, title: str) -> Notification | None:
        with self._lock:
            user_notifications = self._notifications.get(user_id)
            if user_notifications is None:
                return None

            return user_notifications.pop(title.lower(), None)
