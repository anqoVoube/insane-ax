from abc import abstractmethod, ABC

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from utils.raw_sqlalchemy.base import BaseRawSQLHandler


class AbstractDelete(ABC):
    @abstractmethod
    async def execute(self):
        pass


class Delete(BaseRawSQLHandler, AbstractDelete):
    def __init__(self, db: AsyncSession, query: str, **kwargs):
        super().__init__(query, **kwargs)
        self._db = db

    async def execute(self) -> None:
        await self.check_parameters()
        await self._db.execute(text(self._query), self._kwargs)
        await self._db.commit()
