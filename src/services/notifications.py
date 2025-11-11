from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_async_session
from src.repositories.notifications.model import Notification, NotificationStatus
from src.repositories.notifications.repository import NotificationRepository
from src.repositories.users.repository import UserRepository


class NotificationService:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session
        self.notification_repo = NotificationRepository(session)
        self.user_repo = UserRepository(session)

    async def create_notification(self, user_uid: UUID, content: str, channel: str) -> Notification:
        user = await self.user_repo.get_by_uid(user_uid)
        if not user:
            raise ValueError(f'User {user_uid} not found')

        notification = Notification(
            user_uid=user_uid, content=content, channel=channel, status=NotificationStatus.PENDING
        )
        await self.notification_repo.create(notification)
        return notification
