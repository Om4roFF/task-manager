from typing import List

from fastapi import APIRouter

from core.security import *
from endpoints.depends import *
from models.admin import Admin, AdminReg, AdminIn
from models.company import Company
from models.token import Token
from models.user import UserOut, User
from repositories.admin_repository import AdminRepository
from repositories.user_repository import UserRepository

router = APIRouter()


@router.post('/')
async def login_admin(form_data: AdminIn,
                      admin_repo: AdminRepository = Depends(get_admin_repository),
                      company_repo: CompanyRepository = Depends(get_company_repository)):
    user_dict = await admin_repo.get_admin(Admin(email=form_data.username, hashed_password=form_data.password), )
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    company = await company_repo.get_company_by_id(user_dict.company_id)
    hashed_password = verify_password(form_data.password, user_dict.hashed_password)
    if not hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect password")
    access_token = await create_access_token({'sub': user_dict.email})
    return Token(access_token=access_token, token_type='Bearer', company_code=company.code)


@router.post('/create')
async def create_admin(admin_in: AdminReg, admin_repo: AdminRepository = Depends(get_admin_repository),
                       company_repo: CompanyRepository = Depends(get_company_repository)):
    if admin_in.password1 != admin_in.password2:
        raise HTTPException(status_code=400, detail='Password doesnt match')
    company = await company_repo.create(Company(code=admin_in.company_code))
    return await admin_repo.create(admin_in, company.id)


@router.post('/update-code')
async def update_company_code(company: Company, admin: Admin = Depends(get_admin),
                              company_repo: CompanyRepository = Depends(get_company_repository)):
    company.id = admin.company_id
    await company_repo.update(company)
    return company.code


@router.post('/update_user')
async def update_user_info(user: User, admin: Admin = Depends(get_admin),
                           users: UserRepository = Depends(get_user_repository)):
    updated_user = await users.update(u=user)
    print(updated_user)
    return updated_user


@router.get('/users', response_model=List[User])
async def get_all_users_company(admin: Admin = Depends(get_admin),
                                users: UserRepository = Depends(get_user_repository), ):
    all_users = await users.get_all_by_company(admin.company_id)
    return all_users


@router.get('/users/session/')
async def get_user_session(user_id, admin: Admin = Depends(get_admin),
                           session_repo: SessionRepository = Depends(get_session_repository)):
    sessions = await session_repo.get_session_by_user_id(user_id=int(user_id))
    return sessions
