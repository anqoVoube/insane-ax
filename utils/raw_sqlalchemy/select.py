from abc import abstractmethod, ABC
from typing import Any, Tuple

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from utils.raw_sqlalchemy.base import BaseRawSQLHandler


class AbstractSelect(ABC):
    @abstractmethod
    async def fetchall(self) -> Tuple[Any]:
        pass


class Select(BaseRawSQLHandler, AbstractSelect):
    def __init__(self, db: AsyncSession, query: str, **kwargs):
        super().__init__(query, **kwargs)
        self._db = db

    async def fetchall(self):
        await self.check_parameters()
        result = await self._db.execute(text(self._query), self._kwargs)
        return result.fetchall()
