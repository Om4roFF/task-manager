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


@router.post('/update-code/{code}')
async def update_company_code(code: str, admin: Admin = Depends(get_admin),
                              company_repo: CompanyRepository = Depends(get_company_repository)):
    company = Company(code=code, id=admin.id)
    await company_repo.update(company)
    return company.code


@router.post('/update_user')
async def update_user_info(user: User, admin: Admin = Depends(get_admin),
                           users: UserRepository = Depends(get_user_repository)):
    updated_user = await users.update(u=user)
    return updated_user


@router.get('/users', response_model=List[User])
async def get_all_users_company(admin: Admin = Depends(get_admin),
                                users: UserRepository = Depends(get_user_repository),
                                session_repo: SessionRepository = Depends(get_session_repository)):
    all_users = await users.get_all_by_company(admin.company_id)
    for user in all_users:
        sessions = await session_repo.get_session_by_user_id(user_id=user.id)
        time_in_hours = 0
        for session in sessions:
            if session.finished_at is not None:
                dif = session.finished_at - session.started_at
                hours = dif.seconds / 3600
                time_in_hours += hours
        if user.money_in_hour_kzt is not None:
            user.total_money_in_kzt = user.money_in_hour_kzt * time_in_hours

    return all_users


@router.get('/users/session/{user_id}')
async def get_user_session(user_id: int, admin: Admin = Depends(get_admin),
                           session_repo: SessionRepository = Depends(get_session_repository)):
    sessions = await session_repo.get_session_by_user_id(user_id=int(user_id))
    return sessions


@router.get('/boards')
async def get_all_board(admin: Admin = Depends(get_admin), board_repo: BoardRepository = Depends(get_board_repository),
                        users: UserRepository = Depends(get_user_repository),
                        user_group_repo: UserGroupRepository = Depends(get_user_group_repository)):
    await board_repo.get_board_by_company(company_id=1)