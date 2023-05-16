import re
from abc import ABC


class AbstractRawSQLHandler(ABC):
    async def fetch_parameters(self):
        pass

    async def check_parameters(self):
        pass


class BaseRawSQLHandler(AbstractRawSQLHandler):
    def __init__(self, query: str, **kwargs):
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
