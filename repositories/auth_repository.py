from datetime import datetime

from db.auth import auth
from models.user import UserIn
from repositories.base import BaseRepository


class AuthRepository(BaseRepository):

    async def create_session(self, phone: str, code: int):
        now = datetime.utcnow()
        query = auth.insert().values({'phone': phone, 'code': code, 'created_at': now})
        await self.database.execute(query)

    async def is_verified(self, user: UserIn) -> bool:
        query = auth.select().where(auth.c.phone == user.phone and auth.c.code == user.code)
        session = await self.database.fetch_one(query)
        if session is None:
            return False
        query = auth.update().where(auth.c.id == session.get('id'))
        await self.database.execute(query)
        return True
