from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from models.user import User, UserIn
from repositories.auth_repository import AuthRepository
from repositories.user_repository import UserRepository
from services.sms_service import send_sms, generate_code
from .depends import get_user_repository, get_auth_repository

router = APIRouter()


@router.get('/', response_model=List[User])
async def read_users(users: UserRepository = Depends(get_user_repository), ):
    return await users.get_all()


@router.post('/auth', response_model=UserIn)
async def login_user(user: UserIn, users: UserRepository = Depends(get_user_repository),
                     auth: AuthRepository = Depends(get_auth_repository)):
    if user.phone is not None and validate_phone(phone=user.phone):
        is_user = await users.get_by_phone(user.phone)
        if is_user:
            user_response = await users.verify_user(user)
            await verification(user, auth)
        else:
            user_response = await users.create(user)
            await verification(user, auth)
        return status.HTTP_200_OK, user_response
    else:
        return status.HTTP_400_BAD_REQUEST, 'Invalid phone number'


async def verification(user: UserIn, auth: AuthRepository):
    gen_code = await generate_code()
    await auth.create_session(phone=user.phone, code=gen_code)
    await send_sms(phone=user.phone, message=f'Ваш код подтверждения: {gen_code}')


@router.post('/auth/verify', response_model=UserIn)
async def verify(user: UserIn, users: UserRepository = Depends(get_user_repository), ):
    pass


def validate_phone(phone: str) -> bool:
    return True
