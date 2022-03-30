import datetime
from typing import Optional

from pydantic import BaseModel


class Board(BaseModel):
    id: Optional[int] = None
    group_id: int
    description: int
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]
