from typing import Optional

from pydantic import BaseModel


class Company(BaseModel):
    id: Optional[int]
    code: str
