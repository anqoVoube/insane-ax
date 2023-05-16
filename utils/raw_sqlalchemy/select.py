from abc import abstractmethod, ABC
import re
from typing import Any, Tuple

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession



class AbstractSelect(ABC):

    @abstractmethod
    async def fetch_parameters(self):
        pass

    @abstractmethod
    async def check_parameters(self):
        pass

    @abstractmethod
    async def fetchall(self) -> Tuple[Any]:
        pass


class Select(AbstractSelect):
    def __init__(self, db: AsyncSession, query: str, **kwargs):
        self._db = db
        self._query = query
        self._kwargs = kwargs

    async def fetch_parameters(self):
        pattern = r":(\w+)"
        matches = re.findall(pattern, self._query)
        return matches

    async def check_parameters(self):
        parameters = await self.fetch_parameters()
        for parameter in parameters:
            if parameter not in self._kwargs:
                raise KeyError(
                    f"Query parameter `{parameter}` not found after initializing {self.__class__.__name__}"
                )

    async def fetchall(self):
        await self.check_parameters()
        result = await self._db.execute(text(self._query), self._kwargs)
        return result.fetchall()
