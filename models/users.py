import uuid

from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils import UUIDType

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(
        UUIDType(binary=False),
        primary_key=True,
        default=uuid.uuid4
    )
    is_active = Column(Boolean, default=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


PydanticUser = sqlalchemy_to_pydantic(User)
