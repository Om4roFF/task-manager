import datetime

from db.auth import auth
from models.user import UserAuth, UserVerify
from repositories.base import BaseRepository
from sqlalchemy import and_


class AuthRepository(BaseRepository):

    async def create_session(self, phone: str, code: int):
        now = datetime.datetime.utcnow()
        query = auth.insert().values({'phone': phone, 'code': code, 'created_at': now})
        await self.database.execute(query)
        return True

    async def is_verified(self, user: UserVerify) -> bool:
        now = datetime.datetime.utcnow()
        query = auth.select().where(
            and_(auth.c.phone == user.phone, now - auth.c.created_at < datetime.timedelta(seconds=120))).order_by(
            auth.c.created_at.desc())
        session = await self.database.fetch_one(query)
        if session is None:
            return False
        print(session.get('id'))
        if session.get('code') == user.code:
            query = auth.update().where(session.get('id') == auth.c.id)
            values = {'is_used': True}
            await self.database.execute(query, values=values)
            return True
        return False

    async def remove_old_sessions(self, user: UserVerify):
        query = auth.delete().where(and_(auth.c.phone == user.phone, auth.c.code != user.code))
        await self.database.execute(query)
