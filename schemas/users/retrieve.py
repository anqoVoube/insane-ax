from pydantic import BaseModel


class UserRetrieveSchema(BaseModel):
    is_active: bool
    first_name: str
    last_name: str



