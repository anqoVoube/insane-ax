from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL = "postgresql+asyncpg://postgres:1@postgres:5434/db"
    TEST_DATABASE_URL = "postgresql+asyncpg://postgres:1@testdb:5432/test"


settings = Settings()
