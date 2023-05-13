from pydantic import BaseModel


class CreateSchema(BaseModel):
    first_name: str
    last_name: str
