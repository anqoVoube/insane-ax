from sqlalchemy.ext.asyncio import AsyncSession

from schemas.users.where_condition import WhereByID
from utils.raw_sqlalchemy.delete import Delete


async def delete(user_id: str, db: AsyncSession) -> None:
    where = WhereByID(id=user_id)

    from utils.helpers import create_query_for_delete

    query = await create_query_for_delete("users")
    await Delete(db, query, **where.dict()).execute()
