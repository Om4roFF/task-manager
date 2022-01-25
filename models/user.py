from pydantic import BaseModel, EmailStr, validator, constr
from typing import Optional
from datetime import datetime


class User(BaseModel):
    id: Optional[int] = None
    email: EmailStr
    is_verified_email: bool
    hashed_password: str
    phone: str
    is_verified_phone: bool
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
    password: constr(min_length=8)
    password2: str

    @validator('password2')
    def password_match(self, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError("passwords don't match")
        return v
