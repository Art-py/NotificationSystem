from typing import TYPE_CHECKING

from sqlalchemy import ARRAY, Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.repositories.core.base_model import BaseModel, TimestampsMixin
from src.repositories.users.enum import NotificationChannel

if TYPE_CHECKING:
    from src.repositories.notifications.model import Notification


class User(BaseModel, TimestampsMixin):
    """Модель пользователя системы уведомлений"""

    first_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True, doc='Имя')
    last_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True, doc='Фамилия')

    email: Mapped[str | None] = mapped_column(String(320), nullable=True, unique=True, doc='Адрес электронной почты')
    phone: Mapped[str | None] = mapped_column(String(32), nullable=True, unique=True, doc='Номер телефона')
    telegram_id: Mapped[str | None] = mapped_column(String(64), nullable=True, unique=True, doc='Телеграмм id')

    preferred_channels: Mapped[list[NotificationChannel]] = mapped_column(
        ARRAY(Enum(NotificationChannel, name='notification_channel')),
        nullable=False,
        default=lambda: [NotificationChannel.EMAIL, NotificationChannel.SMS, NotificationChannel.TELEGRAM],
        doc='Порядок предпочтительных каналов уведомлений',
    )

    notifications: Mapped[list['Notification']] = relationship('Notification', back_populates='user')
