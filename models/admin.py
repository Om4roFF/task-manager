from typing import Optional

from pydantic import BaseModel


class Admin(BaseModel):
    id: Optional[int]
    email: str
    hashed_password: Optional[str]


class AdminReg(BaseModel):
    id: Optional[int]
    email: str
    password1: str
    password2: str


class AdminIn(BaseModel):
    username: str
    password: str
