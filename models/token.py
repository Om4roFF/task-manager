from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str
    is_exist: bool


class Login(BaseModel):
    phone_number: str
