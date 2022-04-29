import io
import os
from typing import List

import aiofiles as aiofiles
import numpy as np
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from pydub import AudioSegment

from core.config import DATA_DIR
from core.security import create_access_token, get_current_user
from models.token import Token
from models.user import User, UserAuth, UserVerify, UserOut
from repositories.auth_repository import AuthRepository
from repositories.company_repository import CompanyRepository
from repositories.user_repository import UserRepository
from services.sms_service import generate_code
from voice_auth.predictions import get_embeddings, get_cosine_distance
from voice_auth.preprocessing import extract_fbanks
from .depends import get_user_repository, get_auth_repository, get_company_repository

router = APIRouter()

THRESHOLD = 0.45


@router.get('/', response_model=User)
async def get_user(users: User = Depends(get_current_user), ):
    return users


@router.get('/all', response_model=List[UserOut])
async def get_all_users_company(user: User = Depends(get_current_user),
                                users: UserRepository = Depends(get_user_repository), ):
    all_users = await users.get_all_by_company(user.company_id)
    users_out = []
    for usr in all_users:
        users_out.append(UserOut(id=usr.id, phone=usr.phone, image_url=usr.image_url))
    return users_out


@router.put('/')
async def update_user(user: User, user_token: User = Depends(get_current_user),
                      users: UserRepository = Depends(get_user_repository)):
    updated_user = await users.update(u=user)
    return updated_user


@router.post('/test/')
async def test():
    raise HTTPException(status_code=404, detail="Item not found")


@router.post('/auth', response_model=UserAuth)
async def login_user(user: UserAuth, users: UserRepository = Depends(get_user_repository),
                     auth: AuthRepository = Depends(get_auth_repository),
                     company: CompanyRepository = Depends(get_company_repository)):
    is_exist_company = await company.get_company_by_code(user.company_code)
    if is_exist_company is None:
        raise HTTPException(status_code=400, detail='Company doesn\'t exist')
    if user.phone is not None and validate_phone(user.phone):
        code = await verification(user, auth)
        return UserAuth(phone=user.phone, company_code=user.company_code, sms_code=code)
    else:
        raise HTTPException(status_code=401, detail='Invalid phone number')


async def verification(user: UserAuth, auth: AuthRepository):
    gen_code = await generate_code()
    print(gen_code)
    await auth.create_session(phone=user.phone, code=gen_code)
    # await send_sms(phone=user.phone, message=f'Ваш код подтверждения: {gen_code}')
    return gen_code


@router.post('/auth/verify', response_model=Token)
async def verify(user: UserVerify,
                 auth: AuthRepository = Depends(get_auth_repository),
                 users: UserRepository = Depends(get_user_repository),
                 company: CompanyRepository = Depends(get_company_repository)):
    is_exist_company = await company.get_company_by_code(user.company_code)
    if is_exist_company is None:
        raise HTTPException(status_code=400, detail='Company doesn\'t exist')
    is_user_exist = await users.get_by_phone(phone=user.phone)
    if is_user_exist is None:
        await users.create(UserAuth(phone=user.phone, company_code=user.company_code, ),
                           company_id=is_exist_company.id)
    is_verified = await auth.is_verified(user)
    if is_verified:
        access_token = await create_access_token({'sub': user.phone})
        flag = False
        if is_user_exist is not None:
            flag = True
        return Token(access_token=access_token, token_type='Bearer', is_exist=flag)
    raise HTTPException(status_code=400, detail='Incorrect SMS or phone')


@router.post("/voice/register")
async def register_voice(phone: str, voice: UploadFile):
    await validate_audio(phone, voice)
    filename = await _save_file(voice, phone)
    await register_fbank(filename, phone)
    return True


async def register_fbank(filename: str, phone: str):
    fbanks = extract_fbanks(filename)
    embeddings = get_embeddings(fbanks)
    mean_embeddings = np.mean(embeddings, axis=0)
    np.save(DATA_DIR + phone + '/embeddings.npy', mean_embeddings)


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
    if not os.path.exists(dir_):
        os.makedirs(dir_)

    temp_file = dir_ + f'/temp.{file.content_type[6:]}'
    async with aiofiles.open(temp_file, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)

    filename = DATA_DIR + phone + f'/sample.wav'
    song = AudioSegment.from_file(temp_file)
    song.export(filename, format='wav')

    return filename


def validate_phone(phone: str) -> bool:
    if len(phone) == 11 and phone.isdigit():
        value = phone[:2]
        if value == "77":
            return True
    return False


async def validate_audio(phone: str, voice: UploadFile, from_login: bool = False):
    if voice.content_type != 'audio/mp4':
        raise HTTPException(status_code=400, detail='incorrect content type')
    if from_login:
        if not os.path.exists(DATA_DIR + phone) or not os.path.exists(DATA_DIR + phone + '/embeddings.npy') \
                or not os.path.exists(DATA_DIR + phone + '/sample.wav'):
            raise HTTPException(status_code=400, detail='user doesn\'t exist')
