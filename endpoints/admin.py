from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from core.security import verify_password
from endpoints.depends import get_admin_repository
from models.admin import Admin
from repositories.admin_repository import AdminRepository

router = APIRouter()


@router.post('/')
async def login_admin(form_data: OAuth2PasswordRequestForm = Depends(),
                      admin_repo: AdminRepository = Depends(get_admin_repository)):
    user_dict = await admin_repo.get_admin(Admin(email=form_data.username, hashed_password=form_data.password))
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    hashed_password = verify_password(form_data.password, user_dict.hashed_password)
