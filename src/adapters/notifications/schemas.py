from uuid import UUID

from pydantic import BaseModel

from src.repositories.users.enum import NotificationChannel


class NotificationCreate(BaseModel):
    user_uid: UUID
    content: str
    channel: NotificationChannel
