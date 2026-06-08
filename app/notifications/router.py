from fastapi import APIRouter, HTTPException, status

from app.notifications.schemas import (
    NotificationRequest,
    NotificationResponse,
    UserNotificationsResponse,
)
from app.services.engine_registry import notification_engine

router = APIRouter(tags=["notifications"])


@router.post("/notifications/{user_id}", response_model=NotificationResponse)
async def create_notification(
    user_id: str,
    request: NotificationRequest,
) -> NotificationResponse:
    notification = notification_engine.create_notification(
        user_id,
        request.to_notification(),
    )
    return NotificationResponse.from_notification(notification)


@router.get("/notifications/{user_id}", response_model=UserNotificationsResponse)
async def get_notifications(user_id: str) -> UserNotificationsResponse:
    notifications = notification_engine.get_notifications(user_id)
    return UserNotificationsResponse(
        user_id=user_id,
        notifications=[
            NotificationResponse.from_notification(notification)
            for notification in notifications
        ],
    )


@router.get("/notifications/{user_id}/{title}", response_model=NotificationResponse)
async def get_notification(user_id: str, title: str) -> NotificationResponse:
    notification = notification_engine.get_notification(user_id, title)
    if notification is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found",
        )

    return NotificationResponse.from_notification(notification)


@router.put(
    "/notifications/{user_id}/{title}/read",
    response_model=NotificationResponse,
)
async def mark_notification_read(user_id: str, title: str) -> NotificationResponse:
    notification = notification_engine.mark_read(user_id, title)
    if notification is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found",
        )

    return NotificationResponse.from_notification(notification)


@router.delete("/notifications/{user_id}/{title}", response_model=NotificationResponse)
async def delete_notification(user_id: str, title: str) -> NotificationResponse:
    notification = notification_engine.delete_notification(user_id, title)
    if notification is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found",
        )

    return NotificationResponse.from_notification(notification)
