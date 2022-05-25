from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Comment(BaseModel):
    id: Optional[int]
    content: Optional[str]
    user_id: Optional[int]
    task_id: Optional[int]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class CommentIn(BaseModel):
    content: str
    user_id: Optional[int]
    task_id: int
