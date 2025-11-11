from repositories import Notification
from repositories.core.transport import NotificationTransport
from repositories.users.enum import NotificationChannel


class EmailTransport(NotificationTransport):
    def send(self, notification: Notification) -> bool:
        print(f'Отправка email пользователю {notification.user_uid}: {notification.message}')
        return True


class TGTransport(NotificationTransport):
    def send(self, notification: Notification) -> bool:
        print(f'Отправка в ТГ пользователю {notification.user_uid}: {notification.message}')
        return True


class SmsTransport(NotificationTransport):
    def send(self, notification: Notification) -> bool:
        print(f'Отправка SMS пользователю {notification.user_uid}: {notification.message}')
        return True


TRANSPORTS = {
    NotificationChannel.EMAIL: EmailTransport(),
    NotificationChannel.TELEGRAM: TGTransport(),
    NotificationChannel.SMS: SmsTransport(),
}


def send_notification(notification):
    transport = TRANSPORTS.get(notification.channel)
    if not transport:
        print(f'Нет транспорта для канала {notification.channel}')
        return False
    return transport.send(notification)
