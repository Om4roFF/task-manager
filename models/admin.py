from typing import Optional

from pydantic import BaseModel


class Admin(BaseModel):
    id: Optional[int]
    email: str
    hashed_password: Optional[str]
    company_id: Optional[int]


class AdminReg(BaseModel):
    id: Optional[int]
    email: str
    password1: str
    password2: str
    company_code: str


class AdminIn(BaseModel):
    username: str
    password: str
