from fastapi import APIRouter, Depends, HTTPException

from core.security import get_current_user
from endpoints.depends import get_session_repository
from models.user import User
from repositories.session_repository import SessionRepository

router = APIRouter()


@router.get('/')
async def get_my_sessions(user: User = Depends(get_current_user),
                          session_repo: SessionRepository = Depends(get_session_repository)):
    get_sessions = await session_repo.get_session_by_user_id(user.id)


@router.post('/')
async def create_session(user: User = Depends(get_current_user),
                         session_repo: SessionRepository = Depends(get_session_repository)):
    last_session = await session_repo.get_last_session(user.id)

    if last_session is None:
        return await session_repo.create(user.id)
    elif last_session.finished_at is None:
        return await session_repo.set_finish(last_session)
    else:
        return await session_repo.create(user.id)
