from fastapi import APIRouter, Depends, HTTPException

from core.security import get_current_user
from endpoints.depends import *
from models.board import Board, BoardIn, BoardAdd, BoardDel
from models.group import Group
from models.user import User
from models.user_group import UserGroup
from repositories.board_repository import BoardRepository
from repositories.group_repository import GroupRepository
from repositories.user_group_repository import UserGroupRepository

router = APIRouter()


@router.get('/')
async def get_my_boards(user: User = Depends(get_current_user),
                        board_repository: BoardRepository = Depends(get_board_repository),
                        user_group_repo: UserGroupRepository = Depends(get_user_group_repository),
                        task_repo: TaskRepository = Depends(get_task_repository)):
    user_groups = await user_group_repo.get_by_user_id(user_id=user.id)
    my_boards = []
    for ug in user_groups:
        board = await board_repository.get_board_by_group_id(group_id=ug.group_id)
        if board is not None:
            board_tasks = await task_repo.get_task_by_board(board_id=board.id)
            board.tasks = board_tasks
            my_boards.append(board)
    return my_boards


@router.post('/', response_model=Board)
async def create_board(board_in: BoardIn,
                       user: User = Depends(get_current_user),
                       board_repository: BoardRepository = Depends(get_board_repository),
                       group_repo: GroupRepository = Depends(get_group_repository),
                       user_group_repo: UserGroupRepository = Depends(get_user_group_repository)):
    group = Group(name=board_in.group_name)
    group_id = await group_repo.create(group)
    user_group = UserGroup(group_id=group_id.id, user_id=user.id)
    await user_group_repo.create(user_group=user_group)
    board = Board(group_id=group_id.id, description=board_in.description)
    get_board = await board_repository.create(board)
    return get_board


@router.post('/users')
async def add_users_to_board(board_add: BoardAdd, user: User = Depends(get_current_user),
                             board_repository: BoardRepository = Depends(get_board_repository),
                             user_group_repo: UserGroupRepository = Depends(get_user_group_repository)):
    get_board = await board_repository.get_board_by_group_id(board_add.board_id)
    if get_board is not None:
        for usr in board_add.user_ids:
            user_group = UserGroup(group_id=get_board.group_id, user_id=usr)
            exist = await user_group_repo.get_by_user_group(user_id=usr, group_id=get_board.group_id)
            print(exist)
            if exist is None or len(exist) == 0:
                await user_group_repo.create(user_group)
        return 'success'
    raise HTTPException(status_code=400, detail='Fatal error')


@router.post('/delete')
async def delete_board(board_del: BoardDel, user: User = Depends(get_current_user),
                       board_repository: BoardRepository = Depends(get_board_repository), ):
    try:
        board = await board_repository.delete(board_del.board_id)
        if board:
            return 'success'
        raise HTTPException(status_code=400, detail='error')
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail='error')


@router.put('/')
async def update_board(user: User = Depends(get_current_user)):
    pass
