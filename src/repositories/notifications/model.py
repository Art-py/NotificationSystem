import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.repositories.core.base_model import BaseModel, TimestampsMixin
from src.repositories.notifications.enum import NotificationStatus
from src.repositories.users.enum import NotificationChannel

if TYPE_CHECKING:
    from src.repositories.users.model import User


class Notification(BaseModel, TimestampsMixin):
    """Модель уведомления"""

    user_uid: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('users.uid'), nullable=False, index=True, doc='Пользователь, которому отправлено уведомление'
    )
    message: Mapped[str] = mapped_column(String(1024), nullable=False, doc='Текст уведомления')
    status: Mapped[NotificationStatus] = mapped_column(
        Enum(NotificationStatus, name='notification_status'),
        default=NotificationStatus.PENDING,
        nullable=False,
        doc='Статус уведомления',
    )
    sent_channel: Mapped[NotificationChannel | None] = mapped_column(
        Enum(NotificationChannel, name='notification_channel'),
        nullable=True,
        doc='Канал, через который уведомление успешно отправлено',
    )

    user: Mapped['User'] = relationship('User', back_populates='notifications')
