from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from core.security import verify_password, create_access_token, get_admin
from endpoints.depends import get_admin_repository
from models.admin import Admin, AdminReg, AdminIn
from models.token import Token
from repositories.admin_repository import AdminRepository

router = APIRouter()


@router.post('/')
async def login_admin(form_data: AdminIn,
                      admin_repo: AdminRepository = Depends(get_admin_repository)):
    user_dict = await admin_repo.get_admin(Admin(email=form_data.username, hashed_password=form_data.password))
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    hashed_password = verify_password(form_data.password, user_dict.hashed_password)
    if not hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect password")
    access_token = await create_access_token({'sub': user_dict.email})
    return Token(access_token=access_token, token_type='Bearer')


@router.post('/create')
async def create_admin(admin_in: AdminReg, admin_repo: AdminRepository = Depends(get_admin_repository)):
    if admin_in.password1 != admin_in.password2:
        raise HTTPException(status_code=400, detail='Password doesnt match')
    return await admin_repo.create(admin_in)


@router.post('/update_user')
async def update_user_info(admin: Admin = Depends(get_admin), ):
    pass
