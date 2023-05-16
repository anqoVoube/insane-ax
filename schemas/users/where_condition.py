from pydantic import BaseModel


class WhereByID(BaseModel):
    id: str
