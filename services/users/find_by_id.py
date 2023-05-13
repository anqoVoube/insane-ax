from models.users import User


async def find_user_by_id(user_id: int, db):
    if user := await db.query(User).get(user_id):
        return {"full_name": user.full_name}
    return {"error": "Username doesn\'t exist"}
