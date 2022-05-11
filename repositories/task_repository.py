from datetime import datetime
from typing import Optional, List

from db import tasks
from models.task import Task, TaskIn, TaskUpdate
from repositories.base import BaseRepository


class TaskRepository(BaseRepository):

    async def create(self, task: TaskIn) -> Task:
        now = datetime.utcnow()
        item = Task(created_at=now, updated_at=now, description=task.description, status=task.status.upper(),
                    board_id=task.board_id,
                    performer_id=task.performer_id, creator_id=task.creator_id, title=task.title,
                    deadline=task.deadline)
        values = {**item.dict()}
        values.pop("id", None)
        query = tasks.insert().values(**values)
        item.id = await self.database.execute(query)
        return item

    async def update(self, task_update: TaskUpdate) -> Optional[Task]:
        now = datetime.utcnow()
        query = tasks.select().where(tasks.c.id == task_update.id)
        item = await self.database.fetch_one(query)
        if item is None:
            return None
        task = Task.parse_obj(item)
        if task_update.title:
            task.title = task_update.title
        if task_update.status:
            task.status = task_update.status.upper()
        if task_update.description:
            task.description = task_update.description
        if task_update.performer_id:
            task.performer_id = task_update.performer_id
        if task_update.deadline:
            task.deadline = task_update.deadline
        task.updated_at = now
        query = tasks.update().where(tasks.c.id == task.id)
        values = {**task.dict()}
        values.pop("id", None)
        await self.database.execute(query, values=values)
        return task

    async def delete(self, task_id: int) -> bool:
        try:
            query = tasks.delete().where(tasks.c.id == task_id)
            await self.database.execute(query)
            return True
        except:
            return False

    async def get_task_by_id(self, task_id: int) -> Optional[Task]:
        query = tasks.select().where(tasks.c.id == task_id)
        item = await self.database.fetch_one(query)
        if item is None:
            return None
        return Task.parse_obj(item)

    async def get_task_by_board(self, board_id: int) -> List[Task]:
        query = tasks.select().where(tasks.c.board_id == board_id)
        items = await self.database.fetch_all(query)
        if items is None or len(items) == 0:
            return []
        fetched_tasks = []
        for i in items:
            task = Task.parse_obj(i)
            fetched_tasks.append(task)
        return fetched_tasks

    async def get_task_by_performer_id(self, performer_id) -> List[Task]:
        query = tasks.select().where(tasks.c.performer_id == performer_id)
        items = await self.database.fetch_all(query)
        if items is None or len(items) == 0:
            return []
        fetched_tasks = []
        for i in items:
            task = Task.parse_obj(i)
            fetched_tasks.append(task)
        return fetched_tasks

    async def get_task_by_creator_id(self, creator_id) -> List[Task]:
        query = tasks.select().where(tasks.c.creator_id == creator_id)
        items = await self.database.fetch_all(query)
        if items is None or len(items) == 0:
            return []
        fetched_tasks = []
        for i in items:
            task = Task.parse_obj(i)
            fetched_tasks.append(task)
        return fetched_tasks

    async def delete_board(self, task_id):
        try:
            query = tasks.delete().where(tasks.c.id == task_id)
            await self.database.execute(query)
            return True
        except:
            return False
