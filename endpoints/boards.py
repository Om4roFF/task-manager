from fastapi import APIRouter, Depends

from core.security import get_current_user
from models.user import User

router = APIRouter()


@router.get('/')
async def get_my_boards(user: User = Depends(get_current_user)):
    pass


@router.post('/')
async def create_board(user: User = Depends(get_current_user)):
    pass


@router.post('/delete')
async def delete_board(user: User = Depends(get_current_user)):
    pass


@router.put('/update')
async def update_board(user: User = Depends(get_current_user)):
    pass

