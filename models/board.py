import datetime
from typing import Optional, List

from pydantic import BaseModel

from models.task import Task


class Board(BaseModel):
    id: Optional[int] = None
    group_id: int
    description: str
    tasks: List[Task] = []
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]


class BoardIn(BaseModel):
    group_name: Optional[str]
    description: str


class BoardAdd(BaseModel):
    board_id: int
    user_ids: List[int]


class BoardDel(BaseModel):
    board_id: int