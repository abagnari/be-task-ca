from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite+aiosqlite:///:memory:"


settings = Settings()
