from typing import Optional

from pydantic import BaseModel


class UserGroup(BaseModel):
    id: Optional[int]
    group_id: int
    user_id: int
