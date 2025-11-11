from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent


class CoreBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=f'{BASE_DIR}/environment/.env', extra='ignore')


class PostgresSettings(CoreBaseSettings):
    POSTGRES_USER: str = ''
    POSTGRES_PASSWORD: SecretStr = ''
    POSTGRES_DB: str = ''
    POSTGRES_HOST: str = ''
    POSTGRES_PORT: int = 5432

    @property
    def POSTGRES_ASYNC_URL(self) -> str:
        return (
            f'postgresql+asyncpg://{self.POSTGRES_USER}'
            f':{self.POSTGRES_PASSWORD.get_secret_value()}'
            f'@{self.POSTGRES_HOST}'
            f':{self.POSTGRES_PORT}'
            f'/{self.POSTGRES_DB}'
        )


class RedisSettings(CoreBaseSettings):
    REDIS_HOST: str = 'redis'
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: SecretStr | None = None

    @property
    def REDIS_URL(self) -> str:
        password_part = f':{self.REDIS_PASSWORD.get_secret_value()}@' if self.REDIS_PASSWORD else ''
        return f'redis://{password_part}{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}'


class Settings(CoreBaseSettings):
    DEBUG: bool = True
    SECRET_KEY_PASSWORD: SecretStr = ''

    postgres: PostgresSettings = PostgresSettings()
    redis: RedisSettings = RedisSettings()


settings = Settings()
