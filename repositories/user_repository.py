import datetime

from db import users
from models.user import UserAuth, User, UserVerify
from repositories.base import BaseRepository
from typing import List, Optional
from datetime import datetime


class UserRepository(BaseRepository):

    async def get_all(self, limit: int = 100):
        query = users.select().limit(limit)
        return await self.database.fetch_all(query)

    async def get_by_id(self, user_id: int) -> Optional[User]:
        query = users.select().where(users.c.id == user_id)
        user = await self.database.fetch_one(query)
        if user is None:
            return None
        return User.parse_obj(user)

    async def create(self, u: UserAuth) -> User:
        now = datetime.utcnow()
        user = User(phone=u.phone, created_at=now, updated_at=now,
                    last_visit_time=now)
        values = {**user.dict()}
        values.pop("id", None)
        query = users.insert().values(**values)
        user.id = await self.database.execute(query)
        return user

    async def update(self, u: UserAuth) -> User:
        now = datetime.utcnow()
        user = User(phone=u.phone, updated_at=now,
                    last_visit_time=now)
        query = users.update().where(users.c.phone == u.phone)
        values = {**user.dict()}
        values.pop("created_at", None)
        values.pop("id", None)

        values = {'updated_at': datetime.datetime.now()}

        await self.database.execute(query, values=values)
        return user

    async def verify_user(self, u: UserVerify, is_verified: bool = False) -> User:
        now = datetime.utcnow()
        user = User(phone=u.phone, updated_at=now,
                    last_visit_time=now)
        query = users.update().where(users.c.phone == u.phone)
        values = {**user.dict()}
        values.pop("created_at", None)
        values.pop("id", None)

        await self.database.execute(query, values=values)
        return user

    async def get_by_phone(self, phone: str) -> Optional[User]:
        query = users.select().where(users.c.phone == phone)
        user = await self.database.fetch_one(query)
        if user is None:
            return None
        return User.parse_obj(user)

    async def is_user_exist_by_phone(self, phone: str) -> bool:
        query = users.select().where(users.c.phone == phone)
        user = await self.database.fetch_one(query)
        if user is None:
            return False
        return True
