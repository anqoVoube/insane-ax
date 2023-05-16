from fastapi import APIRouter, Depends

from core.database import get_session
from schemas.users import CreateSchema
from services.users import fetch_all
from services.users.create import create_user
from services.users.find_by_id import find_user_by_id

user_router = APIRouter()


@user_router.post("/create/")
async def create(body: CreateSchema, db=Depends(get_session)):
    await create_user(body, db)
    return {"success": "Success!"}


@user_router.get("/find/{user_id}")
async def find_by_id(user_id: str, db=Depends(get_session)):
    return await find_user_by_id(user_id, db)


@user_router.get("/all/")
async def get_all(db=Depends(get_session)):
    return await fetch_all(db)
