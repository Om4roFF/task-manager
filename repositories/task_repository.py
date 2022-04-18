from datetime import datetime
from typing import Optional

from db import tasks
from models.task import Task, TaskIn
from repositories.base import BaseRepository


class TaskRepository(BaseRepository):

    async def create(self, task: TaskIn) -> Task:
        now = datetime.utcnow()
        item = Task(created_at=now, updated_at=now, description=task.description, status=task.status,
                    board_id=task.board_id,
                    performer_id=task.performer_id, creator_id=task.creator_id, title=task.title,
                    deadline=task.deadline)
        values = {**item.dict()}
        values.pop("id", None)
        query = tasks.insert().values(**values)
        item.id = await self.database.execute(query)
        return item

    async def update(self, task: TaskIn) -> Optional[Task]:
        now = datetime.utcnow()
        item = Task(created_at=now, updated_at=now, description=task.description, status=task.status,
                    board_id=task.board_id,
                    performer_id=task.performer_id, creator_id=task.creator_id, title=task.title,
                    deadline=task.deadline)
        if item.id is None:
            return None
        query = tasks.update().where(tasks.c.id == tasks.id)
        values = {**item.dict()}
        values.pop("created_at", None)
        values.pop("id", None)
        await self.database.execute(query, values=values)
        return item

    async def delete(self, board_id: int) -> bool:
        try:
            query = tasks.delete().where(tasks.c.id == board_id)
            await self.database.execute(query)
            return True
        except:
            return False

    async def get_task_by__id(self, task_id: int) -> Optional[Task]:
        query = tasks.select().where(tasks.c.group_id == task_id)
        item = await self.database.fetch_one(query)
        if item is None:
            return None
        return Task.parse_obj(item)

    async def get_board_by__id(self, id: int) -> Optional[Task]:
        query = tasks.select().where(tasks.c.id == id)
        item = await self.database.fetch_one(query)
        if item is None:
            return None
        return Task.parse_obj(item)

    async def delete_board(self, task_id):
        try:
            query = tasks.delete().where(tasks.c.id == task_id)
            await self.database.execute(query)
            return True
        except:
            return False
