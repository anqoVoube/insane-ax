from models.users import User


async def create_user(body, db):
    user = User(**body.dict())
    db.add(user)
    await db.commit()
