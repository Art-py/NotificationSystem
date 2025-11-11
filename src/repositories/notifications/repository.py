import uuid

from sqlalchemy import select, update

from repositories import Notification
from repositories.core.base_repository_model import BaseRepository
from repositories.notifications.enum import NotificationStatus
from repositories.users.enum import NotificationChannel


class NotificationRepository(BaseRepository):
    """Репозиторий уведомлений"""

    async def get_by_uid(self, notification_uid: uuid.UUID) -> Notification | None:
        """Получить уведомление по UID"""
        result = await self._session.execute(
            select(Notification).where(Notification.uid == notification_uid)
        )
        return result.scalar_one_or_none()

    async def get_by_user(self, user_uid: uuid.UUID) -> list[Notification]:
        """Получить все уведомления пользователя"""
        result = await self._session.execute(
            select(Notification).where(Notification.user_uid == user_uid)
        )
        return list(result.scalars())

    async def create(self, notification: Notification) -> Notification:
        """Создать новое уведомление"""
        self._session.add(notification)
        await self._session.flush()
        return notification

    async def update_status(
        self,
        notification_uid: uuid.UUID,
        status: NotificationStatus,
        sent_channel: NotificationChannel | None = None,
    ) -> None:
        """Обновить статус и (опционально) канал отправки"""
        stmt = (
            update(Notification)
            .where(Notification.uid == notification_uid)
            .values(status=status, sent_channel=sent_channel)
        )
        await self._session.execute(stmt)
        await self._session.flush()
