from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from core.database import get_session
from core.settings import settings
from main import app
from models.users import Base

SQLALCHEMY_DATABASE_URL = settings.TEST_DATABASE_URL

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def create_all_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_all_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def override_get_session() -> AsyncSession:
    async with async_session() as session:
        await create_all_tables()
        yield session
        # await drop_all_tables()


app.dependency_overrides[get_session] = override_get_session


client = TestClient(app)
