from sqlalchemy.ext.asyncio import AsyncSession

from schemas.users.where_condition import WhereByID
from utils.raw_sqlalchemy.update import Update


async def change(data: dict, user_id: str, db: AsyncSession) -> None:
    where = WhereByID(id=user_id)

    from utils.helpers import create_query_for_update

    query = await create_query_for_update("users", data)
    await Update(db, query, **data, **where.dict()).execute()
