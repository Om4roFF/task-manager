from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Session(BaseModel):
    id: Optional[int]
    user_id: int
    started_at: Optional[datetime]
    finished_at: Optional[datetime]
