from typing import Any, List, Iterable, Tuple, Union, Optional, Type

from sqlalchemy.engine import Row
from sqlalchemy.exc import DBAPIError

from utils.exceptions.does_not_exist import DoesNotExist
from utils.exceptions.validation import ValidationError
from utils.raw_sqlalchemy.select import AbstractSelect
from pydantic import BaseModel


class Getter:
    """
    Handles db's retrieved queryset with check for empty and multiple object response.

    Args:
        - data: Response (using .fetchall) from DB
    """
    def __init__(self, data: Tuple[Any], map_to: Type[BaseModel], on_error_message: Optional[str] = "Doesn't Exist"):
        self._data = data
        self._map_to = map_to
        self._error_message = on_error_message

    async def map_instance(self, response):
        return self._map_to(
            **{field: value for field, value in zip(response.keys(), response)}
        )

    @classmethod
    async def from_selector(
            cls,
            selector: AbstractSelect,
            map_to: Type[BaseModel],
            on_error_message: Optional[str] = "Doesn't Exist"
    ):
        try:
            data = await cls._get_data_from_selector(selector)
        except DBAPIError:
            raise ValidationError(on_error_message)
        return cls(data, map_to, on_error_message)

    @staticmethod
    async def _get_data_from_selector(selector):
        return await selector.fetchall()


class GetOne(Getter):
    async def check_is_one(self) -> None:
        """
        Checks whether instance exists

        raises: DoesNotExist in empty queryset (response)
        """
        if not len(self._data):
            raise ValidationError(self._error_message)

    async def get_first_in_pydantic(self) -> Any:
        """
        Retrieves first value from iterable

        :return:
        """
        await self.check_is_one()
        instance = self._data[0]
        return await self.map_instance(instance)


class GetAll(Getter):
    async def get_all_in_pydantic(self):
        return [await self.map_instance(instance) for instance in self._data]
