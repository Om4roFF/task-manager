from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException

from core.security import get_current_user
from endpoints.depends import *
from models.comment import CommentIn
from models.task import TaskIn, TaskOut, Task, TaskUpdate
from models.user import User, UserOut
from repositories.task_repository import TaskRepository
from repositories.user_repository import UserRepository

router = APIRouter()


@router.post('/', response_model=Optional[Task])
async def create_task(task_in: TaskIn, user: User = Depends(get_current_user),
                      task_repository: TaskRepository = Depends(get_task_repository)):
    try:
        task_in.creator_id = user.id
        task = await task_repository.create(task_in)
        return task
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=400)


@router.put('/')
async def update(task_in: TaskUpdate, user: User = Depends(get_current_user),
                 task_repository: TaskRepository = Depends(get_task_repository)):
    try:
        if task_in.status is not None and task_in.status.upper() != 'TODO' and task_in.status.upper() != 'IN_PROCESS' and\
                task_in.status.upper() != 'DONE' and task_in.status.upper() != 'UNDETERMINED':
            raise HTTPException(detail='Invalid status', status_code=400)
        print('here')
        updated_task = await task_repository.update(task_in)
        if updated_task is None:
            raise HTTPException(detail='Invalid input', status_code=400)
        return updated_task
    except HTTPException as e:
        raise HTTPException(detail=e.detail, status_code=400)
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=400)


@router.delete('/{task_id}')
async def delete(task_id: int, user: User = Depends(get_current_user),
                 task_repository: TaskRepository = Depends(get_task_repository)):
    await task_repository.delete(task_id)
    return True


@router.get('/', response_model=Optional[TaskOut])
async def get_task(task_id: int = None,
                   user: User = Depends(get_current_user),
                   task_repository: TaskRepository = Depends(get_task_repository),
                   user_repo: UserRepository = Depends(get_user_repository)):
    if task_id is None:
        raise HTTPException(detail='query parameters are empty', status_code=400)
    try:
        task = await task_repository.get_task_by_id(task_id)
        if task is None:
            raise HTTPException(detail='error: task_id is incorrect', status_code=400)
        performer = await user_repo.get_by_id(task.performer_id)
        performer_out = None
        if performer is not None:
            performer_out = UserOut(id=performer.id, phone=performer.phone, image_url=performer.image_url)
        creator = await user_repo.get_by_id(task.creator_id)
        task_out = TaskOut(id=task.id, title=task.title, description=task.description, status=task.status,
                           deadline=task.deadline, board_id=task.board_id,
                           performer=performer_out, creator=creator, created_at=task.created_at,
                           updated_at=task.updated_at)
        return task_out
    except Exception as e:
        raise HTTPException(detail=f'error: {str(e)}', status_code=400)


@router.get('/for-me', response_model=List[TaskOut])
async def get_by_performer(user: User = Depends(get_current_user),
                           task_repo: TaskRepository = Depends(get_task_repository),
                           user_repo: UserRepository = Depends(get_user_repository)):
    tasks = await task_repo.get_task_by_performer_id(user.id)
    if not tasks:
        return []

    output_tasks = []
    for task in tasks:
        performer = await user_repo.get_by_id(task.performer_id)
        creator = await user_repo.get_by_id(task.creator_id)
        task_out = await get_task_out(task, creator, performer)
        output_tasks.append(task_out)
    return output_tasks


@router.get('/my', response_model=List[TaskOut])
async def get_by_creator(user: User = Depends(get_current_user),
                         task_repo: TaskRepository = Depends(get_task_repository),
                         user_repo: UserRepository = Depends(get_user_repository)):
    tasks = await task_repo.get_task_by_creator_id(user.id)
    if not tasks:
        raise HTTPException(detail='error: creator_id is incorrect', status_code=400)
    output_tasks = []
    for task in tasks:
        performer = await user_repo.get_by_id(task.performer_id)
        creator = await user_repo.get_by_id(task.creator_id)
        task_out = await get_task_out(task, creator, performer)
        output_tasks.append(task_out)
    return output_tasks


async def get_task_out(task: Task, creator: User, performer: User = None, ) -> TaskOut:
    task_out = TaskOut(id=task.id, title=task.title, description=task.description, status=task.status,
                       deadline=task.deadline, board_id=task.board_id,
                       performer=performer, creator=creator, created_at=task.created_at,
                       updated_at=task.updated_at)
    return task_out


@router.post('/comment', )
async def add_comment(comment: CommentIn, user: User = Depends(get_current_user),
                      comment_repo: CommentRepository = Depends(get_comment_repository)):
    comment.user_id = user.id
    await comment_repo.create(comment, user)
    comments = await comment_repo.get_comments_by_task_id(comment.task_id, user)
    return comments


@router.get('/comment/{task_id}')
async def get_comments(task_id: int, user: User = Depends(get_current_user),
                       comment_repo: CommentRepository = Depends(get_comment_repository)):
    comments = await comment_repo.get_comments_by_task_id(task_id, user)
    return comments
