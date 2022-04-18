from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from models.board import Board
from models.user import User


class Task(BaseModel):
    id: Optional[int]
    title: str
    description: str
    status: str
    deadline: Optional[datetime]
    board_id: int
    performer_id: Optional[int]
    creator_id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class TaskIn(BaseModel):
    id: Optional[int]
    title: str
    description: str
    deadline: Optional[datetime]
    board_id: int
    performer_id: Optional[int]
    creator_id: Optional[int]
    status: str = 'TODO'


class TaskOut(BaseModel):
    id: Optional[int]
    title: str
    description: str
    status: str
    deadline: datetime
    board: Board
    performer: User
    creator: User
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
