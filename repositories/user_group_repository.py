from sqlalchemy import and_

from db import user_group_table
from models.user_group import UserGroup
from repositories.base import BaseRepository


class UserGroupRepository(BaseRepository):

    async def create(self, user_group: UserGroup) -> UserGroup:
        values = {**user_group.dict()}
        values.pop("id", None)
        query = user_group_table.insert().values(**values)
        user_group.id = await self.database.execute(query)
        return user_group

    async def delete(self, user_group_id: int):
        try:
            query = user_group_table.delete().where(user_group_table.c.id == user_group_id)
            await self.database.execute(query)
            return True
        except:
            return False

    async def get_by_user_id(self, user_id: int):
        query = user_group_table.select().where(user_group_table.c.user_id == user_id)
        user_groups = await self.database.fetch_all(query)
        print(user_groups)
        if user_groups is None:
            return []
        usrgr = []
        for ug in user_groups:
            usrgr.append(UserGroup.parse_obj(ug))
        return usrgr

    async def get_by_user_group(self, user_id: int, group_id: int):
        query = user_group_table.select().where(
            and_(user_group_table.c.user_id == user_id, user_group_table.c.group_id == group_id))
        user_groups = await self.database.fetch_all(query)
        print(user_groups)
        if user_groups is None:
            return None
        usrgr = []
        for ug in user_groups:
            usrgr.append(UserGroup.parse_obj(ug))
        return usrgr
