import datetime
from typing import Optional, List

from pydantic import BaseModel

from models.group import Group
from models.task import TaskOut
from models.user import User


class Board(BaseModel):
    id: Optional[int] = None
    group_id: int
    description: str
    tasks: List[TaskOut] = []
    users: List[User] = []
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]


class BoardOut(BaseModel):
    id: Optional[int] = None
    group: Group
    description: str
    tasks: List[TaskOut] = []
    users: List[User] = []
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