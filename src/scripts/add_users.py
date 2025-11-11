import asyncio

from db import async_session_local
from src.repositories.users.enum import NotificationChannel
from src.repositories.users.model import User


async def seed_users():
    """Создаёт несколько тестовых пользователей с разными каналами связи"""

    async with async_session_local() as session:
        users_data = [
            {
                'first_name': 'Алексей',
                'last_name': 'Иванов',
                'email': 'ivanov@example.com',
                'phone': '+79001112233',
                'telegram_id': '123456789',
                'preferred_channels': [
                    NotificationChannel.EMAIL,
                    NotificationChannel.TELEGRAM,
                    NotificationChannel.SMS,
                ],
            },
            {
                'first_name': 'Мария',
                'last_name': 'Петрова',
                'email': None,
                'phone': '+79005556677',
                'telegram_id': '987654321',
                'preferred_channels': [
                    NotificationChannel.TELEGRAM,
                    NotificationChannel.SMS,
                ],
            },
            {
                'first_name': 'Дмитрий',
                'last_name': 'Соколов',
                'email': 'sokolov@example.com',
                'phone': None,
                'telegram_id': None,
                'preferred_channels': [NotificationChannel.EMAIL],
            },
            {
                'first_name': 'Елена',
                'last_name': 'Кузнецова',
                'email': None,
                'phone': '+79001234567',
                'telegram_id': None,
                'preferred_channels': [NotificationChannel.SMS],
            },
        ]

        session.add_all([User(**user) for user in users_data])
        await session.commit()

        print(f'{len(users_data)} пользователей добавлено в базу данных.')


if __name__ == '__main__':
    asyncio.run(seed_users())
