import os
from datetime import timedelta
from typing import List, Optional

import aiofiles as aiofiles
import numpy as np
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.security import OAuth2PasswordRequestForm

from core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from core.security import create_access_token, get_current_user, oauth2_scheme, decode_access_token
from models.token import Token
from models.user import User, UserAuth, UserVerify
from repositories.auth_repository import AuthRepository
from repositories.user_repository import UserRepository
from services.sms_service import send_sms, generate_code
from voice_auth.predictions import get_embeddings, get_cosine_distance
from voice_auth.preprocessing import extract_fbanks
from .depends import get_user_repository, get_auth_repository

router = APIRouter()
DATA_DIR = 'data_files/'
THRESHOLD = 0.45

@router.get('/', response_model=User)
async def get_user(users: User = Depends(get_current_user), ):
    return users


@router.post('/test/')
async def test():
    print('hello')
    raise HTTPException(status_code=404, detail="Item not found")


@router.post('/auth', response_model=UserAuth)
async def login_user(user: UserAuth, users: UserRepository = Depends(get_user_repository),
                     auth: AuthRepository = Depends(get_auth_repository)):
    if user.phone is not None and validate_phone(user.phone):
        is_user = await users.is_user_exist_by_phone(user.phone)
        if is_user:
            await verification(user, auth)
        else:
            await users.create(user)
            await verification(user, auth)
        return UserAuth(phone=user.phone)
    else:
        raise HTTPException(status_code=401, detail='Invalid phone number')


async def verification(user: UserAuth, auth: AuthRepository):
    gen_code = await generate_code()
    print(gen_code)
    await auth.create_session(phone=user.phone, code=gen_code)
    # await send_sms(phone=user.phone, message=f'Ваш код подтверждения: {gen_code}')


@router.post('/auth/verify', response_model=Token)
async def verify(user: UserVerify,
                 auth: AuthRepository = Depends(get_auth_repository)):
    is_verified = await auth.is_verified(user)
    if is_verified:
        access_token = await create_access_token({'sub': user.phone})
        print(access_token)
        return Token(access_token=access_token, token_type='Bearer')

    raise HTTPException(status_code=400, detail='Incorrect SMS or phone')


@router.post("/token", response_model=Token)
async def login_for_access_token(token: str = Depends(oauth2_scheme)):
    user = await decode_access_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = await create_access_token(
        data={"sub": user.get('sub')}
    )
    return Token(access_token=access_token, token_type='Bearer')


@router.post("/voice/register")
async def register_voice(phone: str, voice: UploadFile):
    await validate_audio(phone, voice)
    filename = await _save_file(voice, phone)
    fbanks = extract_fbanks(filename)
    embeddings = get_embeddings(fbanks)
    print('shape of embeddings: {}'.format(embeddings.shape), flush=True)
    mean_embeddings = np.mean(embeddings, axis=0)
    np.save(DATA_DIR + phone + '/embeddings.npy', mean_embeddings)
    return True


@router.post("/voice/login")
async def login_voice(phone: str, voice: UploadFile = File(...)):

    await validate_audio(phone, voice, from_login=True)

    filename = await _save_file(voice, phone)
    fbanks = extract_fbanks(filename)
    embeddings = get_embeddings(fbanks)
    stored_embeddings = np.load(DATA_DIR + phone + '/embeddings.npy')
    stored_embeddings = stored_embeddings.reshape((1, -1))

    distances = get_cosine_distance(embeddings, stored_embeddings)
    print('mean distances', np.mean(distances), flush=True)
    positives = distances < THRESHOLD
    positives_mean = np.mean(positives)
    print('positives mean: {}'.format(positives_mean), flush=True)
    if positives_mean >= .65:
        return True
    else:
        raise HTTPException(status_code=400, detail='Incorrect user')


async def _save_file(file: UploadFile, phone):
    dir_ = DATA_DIR + phone
    print(dir_)
    if not os.path.exists(dir_):
        os.makedirs(dir_)

    filename = DATA_DIR + phone + f'/sample.wav'
    async with aiofiles.open(filename, 'wb') as out_file:
        content = await file.read()  # async read
        await out_file.write(content)  # async write
    return filename


def validate_phone(phone: str) -> bool:
    return True


async def validate_audio(phone: str, voice: UploadFile, from_login: bool = False):
    if voice.content_type != 'audio/wav':
        raise HTTPException(status_code=400, detail='incorrect content type')
    if from_login:
        if not os.path.exists(DATA_DIR + phone) or not os.path.exists(DATA_DIR + phone + '/embeddings.npy') \
                or not os.path.exists(DATA_DIR + phone + '/sample.wav'):
            raise HTTPException(status_code=400, detail='user doesn\'t exist')
