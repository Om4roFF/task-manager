import datetime
from typing import Optional

from pydantic import BaseModel


class Board(BaseModel):
    id: Optional[int] = None
    group_id: int
    description: int
    created_id: datetime.datetime
    updated_id: datetime.datetime
