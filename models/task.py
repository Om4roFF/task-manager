from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from models.user import UserOut, User


class Task(BaseModel):
    id: Optional[int]
    title: str
    description: str
    status: str
    deadline: Optional[datetime]
    board_id: int
    performer_id: Optional[int]
    creator_id: int
    is_archived: Optional[bool]
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


class TaskUpdate(BaseModel):
    id: int
    title: Optional[str]
    description: Optional[str]
    deadline: Optional[datetime]
    performer_id: Optional[int]
    status: Optional[str]


class TaskOut(BaseModel):
    id: int
    title: str
    description: str
    status: str
    deadline: Optional[datetime]
    board_id: int
    performer: Optional[User]
    creator: User
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
