from typing import Optional

from pydantic import BaseModel


class Admin(BaseModel):

    id: Optional[int]
    email: str
    hashed_password: str
