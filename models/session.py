from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Session(BaseModel):
    id: Optional[int]
    user_id: int
    latitude: Optional[float]
    longitude: Optional[float]
    started_at: Optional[datetime]
    finished_at: Optional[datetime]


class SessionIn(BaseModel):
    latitude: Optional[float]
    longitude: Optional[float]
