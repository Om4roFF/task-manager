from fastapi import APIRouter, Depends, HTTPException

from core.security import get_current_user
from endpoints.depends import get_task_repository
from models.task import TaskIn
from models.user import User
from repositories.task_repository import TaskRepository

router = APIRouter()


@router.get('/')
async def create_task(task_in: TaskIn, user: User = Depends(get_current_user),
                      task_repository: TaskRepository = Depends(get_task_repository)):
    try:
        task_in.id = user.id
        task = await task_repository.create(task_in)
        return task
    except Exception as e:
        HTTPException(detail=e, status_code=400)


@router.put('/')
async def update(task_in: TaskIn, user: User = Depends(get_current_user),
                      task_repository: TaskRepository = Depends(get_task_repository)):
    try:
        pass
    except Exception as e:
        HTTPException(detail=e, status_code=400)
