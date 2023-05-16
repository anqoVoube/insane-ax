from schemas.users.retrieve import UserRetrieveSchema
from utils.helpers import GetOne
from utils.raw_sqlalchemy.select import Select


async def find_user_by_id(user_id: str, db):

    instance_getter = await GetOne.from_selector(
        selector=Select(
            db, "SELECT * FROM users WHERE id = :user_id", user_id=user_id
        ),
        map_to=UserRetrieveSchema,
        on_error_message="User doesn't exist"
    )
    user_instance = await instance_getter.get_first_in_pydantic()
    return user_instance
