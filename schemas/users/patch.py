from typing import Optional

from pydantic import BaseModel


class UserChangeSchema(BaseModel):
    is_active: Optional[bool]
    first_name: Optional[str]
    last_name: Optional[str]



