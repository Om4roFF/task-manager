import datetime
from typing import Optional

from pydantic import BaseModel


class Group(BaseModel):
    id: Optional[int]
    name: Optional[str]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]