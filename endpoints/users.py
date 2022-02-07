from typing import List

from fastapi import APIRouter, Depends

from models.user import User
from repositories.user_repository import UserRepository
from .depends import get_user_repository

router = APIRouter()


@router.get('/', response_model=List[User])
async def read_users(users: UserRepository = Depends(get_user_repository),):
    return await users.get_all()

