from pydantic import BaseModel, EmailStr, validator, constr
from typing import Optional
from datetime import datetime


class User(BaseModel):
    id: Optional[int] = None
    email: EmailStr
    is_verified_email: bool
    phone: str
    role: str
    position: Optional[str]
    image_url: Optional[str]
    total_money_in_kzt: Optional[int]
    last_visit_time: datetime
    updated_at: datetime
    created_at: datetime


class UserIn(BaseModel):
    email: EmailStr
    phone: str
    image_url: Optional[str]
    code: int

