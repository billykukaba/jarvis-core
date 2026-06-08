from pydantic import BaseModel, Field

from app.notifications.notification_engine import Notification


class NotificationRequest(BaseModel):
    title: str = Field(min_length=1)
    message: str = Field(min_length=1)
    read: bool = False

    def to_notification(self) -> Notification:
        return Notification(
            title=self.title,
            message=self.message,
            read=self.read,
        )


class NotificationResponse(BaseModel):
    title: str
    message: str
    read: bool

    @classmethod
    def from_notification(
        cls,
        notification: Notification,
    ) -> "NotificationResponse":
        return cls(
            title=notification.title,
            message=notification.message,
            read=notification.read,
        )


class UserNotificationsResponse(BaseModel):
    user_id: str
    notifications: list[NotificationResponse]
