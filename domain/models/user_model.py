from typing import Optional

from pydantic import BaseModel


class UserModel(BaseModel):
    user_id: Optional[int]
    document: str
    name: str
