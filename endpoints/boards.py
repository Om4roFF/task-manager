from fastapi import APIRouter, Depends

from core.security import get_current_user
from endpoints.depends import get_board_repository
from models.user import User
from repositories.board_repository import BoardRepository

router = APIRouter()


@router.get('/')
async def get_my_boards(user: User = Depends(get_current_user),
                        board_repository: BoardRepository = Depends(get_board_repository)):
    my_boards = await board_repository.get_board_by_id(user.id)


@router.post('/')
async def create_board(user: User = Depends(get_current_user)):
    pass


@router.post('/delete')
async def delete_board(user: User = Depends(get_current_user)):
    pass


@router.put('/update')
async def update_board(user: User = Depends(get_current_user)):
    pass

