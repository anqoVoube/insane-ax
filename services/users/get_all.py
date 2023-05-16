from sqlalchemy.ext.asyncio import AsyncSession

from schemas.users.retrieve import UserRetrieveSchema
from utils.helpers import GetAll
from utils.raw_sqlalchemy.select import Select


async def fetch_all(db: AsyncSession):
    instance_getter = await GetAll.from_selector(
        selector=Select(
            db, "SELECT * FROM users"
        ),
        map_to=UserRetrieveSchema,
        on_error_message="User doesn't exist"
    )
    user_instance = await instance_getter.get_all_in_pydantic()
    return user_instance
