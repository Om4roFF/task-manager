from datetime import datetime
from typing import Optional

from db import groups
from models.group import Group
from repositories.base import BaseRepository


class GroupRepository(BaseRepository):

    async def create(self, group: Group) -> Group:
        now = datetime.utcnow()
        item = Group(created_at=now, updated_at=now, name=group.name)
        values = {**item.dict()}
        values.pop("id", None)
        query = groups.insert().values(**values)
        item.id = await self.database.execute(query)
        return item

    async def update(self, group: Group) -> Optional[Group]:
        now = datetime.utcnow()
        item = Group(created_at=now, updated_at=now, name=group.name, id=group.id)
        if item.id is None:
            return None
        query = groups.update().where(groups.c.id == group.id)
        values = {**item.dict()}
        values.pop("created_at", None)
        values.pop("id", None)
        await self.database.execute(query, values=values)
        return item

    async def delete(self, group_id: int) -> bool:
        try:
            query = groups.delete().where(groups.c.id == group_id)
            await self.database.execute(query)
            return True
        except:
            return False

    async def get_group_by_id(self, group_id: int):
        query = groups.select().where(groups.c.id == group_id)
        group = await self.database.fetch_one(query)
        if group is None:
            return None
        return Group.parse_obj(group)
