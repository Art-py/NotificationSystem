from abc import ABC, abstractmethod

from src.repositories.notifications.model import Notification


class NotificationTransport(ABC):
    @abstractmethod
    def send(self, notification: Notification) -> bool:
        """Отправить уведомление"""
        pass
