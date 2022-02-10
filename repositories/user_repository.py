import datetime

from db import users
from models.user import UserIn, User
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

    async def create(self, u: UserIn) -> User:
        now = datetime.utcnow()
        user = User(phone=u.phone, created_at=now, updated_at=now,
                    last_visit_time=now, is_verified_phone=False)
        values = {**user.dict()}
        values.pop("id", None)
        query = users.insert().values(**values)
        user.id = await self.database.execute(query)
        return user

    async def update(self, u: UserIn) -> User:
        now = datetime.utcnow()
        user = User(phone=u.phone, updated_at=now,
                    last_visit_time=now, image_url=u.image_url)
        values = {**user.dict()}
        values.pop("created_at", None)
        values.pop("id", None)
        query = users.update().where(users.c.id == id).values(**values)
        await self.database.execute(query)
        return user

    async def verify_user(self, u: UserIn, is_verified: bool = False) -> User:
        now = datetime.utcnow()
        user = User(phone=u.phone, updated_at=now,
                    last_visit_time=now, is_verified_phone=is_verified)
        values = {**user.dict()}
        values.pop("created_at", None)
        values.pop("id", None)
        query = users.update().where(users.c.id == id).values(**values)
        await self.database.execute(query)
        return user

    async def get_by_email(self, email: str) -> Optional[User]:
        query = users.select().where(users.c.email == email)
        user = await self.database.fetch_one(query)
        if user is None:
            return None
        return User.parse_obj(user)

    async def get_by_phone(self, phone: str) -> Optional[User]:
        query = users.select().where(users.c.phone == phone)
        user = await self.database.fetch_one(query)
        if user is None:
            return None
        return User.parse_obj(user)
