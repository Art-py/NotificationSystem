import asyncio

from notifications_transport.transports import send_notification
from src.celery_app import app
from src.db import async_session_local
from src.repositories.notifications.model import NotificationStatus
from src.repositories.notifications.repository import NotificationRepository
from src.repositories.users.repository import UserRepository


@app.task(name='src.tasks.notifications.send_notifications')
async def send_notifications():
    """Отправить все неотправленные уведомления"""
    asyncio.run(_send_notifications_async())


async def _send_notifications_async():
    async with async_session_local() as session:
        notification_repo = NotificationRepository(session)
        user_repo = UserRepository(session)

        pending_notifications = await notification_repo.get_pending_notifications()

        for notification in pending_notifications:
            user = await user_repo.get_by_uid(notification.user_uid)
            if not user:
                continue

            for user_notification in user.preferred_channels:
                success = send_notification(user_notification)
                if success:
                    user_notification.status = NotificationStatus.SENT

            session.commit()
