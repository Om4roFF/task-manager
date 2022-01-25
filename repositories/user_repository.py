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
        query = users.select().where(users.c.id == user_id).first()
        user = await self.database.fetch_one(query)
        if user is None:
            return None
        return User.parse_obj(user)

    async def create(self, u: UserIn) -> User:
        now = datetime.utcnow()
        user = User(email=u.email, phone=u.phone, image_url=u.image_url, created_at=now, updated_at=now,
                    last_visit_time=now, is_verified_email=False)

    async def update(self, u: UserIn) -> User:
        pass

    async def get_by_email(self, email: str) -> Optional[User]:
        query = users.select().where(users.c.email == email).first()
        user = await self.database.fetch_one(query)
        if user is None:
            return None
        return User.parse_obj(user)
