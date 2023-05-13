from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL = "postgresql+asyncpg://postgres:1@localhost:5432/insane"


settings = Settings()
