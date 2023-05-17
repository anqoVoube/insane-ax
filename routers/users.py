from fastapi import APIRouter, Depends
from sqlalchemy import text
from starlette.requests import Request

from core.database import get_session
from schemas.users import CreateSchema
from schemas.users.patch import UserChangeSchema
from schemas.users.retrieve import UserRetrieveSchema
from services.users import fetch_all
from services.users.change import change
from services.users.create import create_user
from services.users.delete import delete
from services.users.find_by_id import find_user_by_id
from utils.helpers import GetAll

user_router = APIRouter()


@user_router.post("/create/", status_code=201)
async def create(body: CreateSchema, db=Depends(get_session)):
    await create_user(body, db)
    return {"success": "Success!"}


@user_router.get("/find/{user_id}", status_code=200)
async def find_by_id(user_id: str, db=Depends(get_session)):
    return await find_user_by_id(user_id, db)


@user_router.get("/all/")
async def get_all(db=Depends(get_session)):
    return await fetch_all(db)


@user_router.post("/change/{user_id}")
async def change_record(request: Request, user_id: str, _: UserChangeSchema, db=Depends(get_session)):
    data = await request.json()
    await change(data, user_id, db)
    return {"success": "Successfully updated"}


@user_router.delete("/delete/{user_id}", status_code=204)
async def delete_by_id(user_id: str, db=Depends(get_session)):
    await delete(user_id, db)


@user_router.get("/", status_code=200)
async def delete_by_id(search: str, db=Depends(get_session)):
    # NO TIME FOR REFACTORING :(
    db_response = await db.execute(
        text("""SELECT * FROM users WHERE CONCAT(first_name, ' ', last_name) LIKE :name"""),
        {"name": f"%{search}%"}
    )
    result = await GetAll(
        data=db_response.fetchall(),
        map_to=UserRetrieveSchema,
        on_error_message="Internal server error"
    ).get_all_in_pydantic()
    return result
