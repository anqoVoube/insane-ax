from typing import Any, Tuple, Optional, Type

from sqlalchemy.exc import DBAPIError

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
            **{field: value for field, value in zip(response._fields, response)}
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


# ----- NOT ENOUGH TIME FOR REFACTORING :(
async def create_query_for_update(table_name: str, data: dict):
    change = ", ".join([f"{key} = :{key}" for key in data.keys()])
    where_query = f"id = :id"
    return f"UPDATE {table_name} SET {change} WHERE {where_query}"


async def create_query_for_delete(table_name: str):
    where_query = f"id = :id"
    return f"DELETE FROM {table_name} WHERE {where_query}"