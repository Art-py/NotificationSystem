from src.celery_app import app
from repositories.users.enum import NotificationChannel
from src.repositories.notifications.repository import NotificationRepository
from src.repositories.users.repository import UserRepository
from src.db import async_session_local
from src.repositories.notifications.model import NotificationStatus
import asyncio


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

            # эмуляция логики отправки (email, push, sms и т.д.)
            notification.status = NotificationStatus.SENT
            notification.sent_channel = NotificationChannel.EMAIL
            await session.commit()
