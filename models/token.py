from typing import Optional

from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str
    is_exist: Optional[bool]
    company_code: Optional[str]


class Login(BaseModel):
    phone_number: str
