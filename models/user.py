from datetime import datetime
from typing import Optional

from pydantic import BaseModel, validator


class User(BaseModel):
    id: Optional[int] = None
    phone: str
    role: Optional[str]
    position: Optional[str]
    name: Optional[str]
    image_url: Optional[str]
    city_id: Optional[int]
    company_id: Optional[int]
    total_money_in_kzt: Optional[int]
    last_visit_time: datetime
    updated_at: datetime
    created_at: Optional[datetime]


class UserOut(BaseModel):
    id: int
    phone: str
    image_url: Optional[str]



class UserAuth(BaseModel):
    phone: str
    company_code: str
    sms_code: Optional[str]

    @validator('phone')
    def name_must_contain_space(cls, v, values, **kwargs):
        if len(v) < 11:
            raise ValueError('incorrect phone number')
        return v.title()


class UserVerify(BaseModel):
    phone: str
    code: int
    company_code: str
