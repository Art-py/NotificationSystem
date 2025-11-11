import uuid

from sqlalchemy import select

from src.repositories.core.base_repository_model import BaseRepository
from src.repositories.users.model import User


class UserRepository(BaseRepository):
    """Репозиторий пользователя"""

    async def get_bu_uid(self, user_uid: uuid.UUID) -> User | None:
        """Получить пользователя по UID"""
        result = await self._session.execute(select(User).where(User.uid == user_uid))
        return result.scalar_one_or_none()

    async def get_all(self) -> list[User]:
        """Получить всех пользователей"""
        result = await self._session.execute(select(User))
        return list(result.scalars())
