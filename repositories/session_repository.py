from datetime import datetime
from typing import List, Optional

from db.sessions import sessions
from models.session import Session
from repositories.base import BaseRepository


class SessionRepository(BaseRepository):

    async def create(self, user_id: int):
        now = datetime.utcnow()
        item = Session(user_id=user_id, started_at=now)
        values = {**item.dict()}
        values.pop("id", None)
        query = sessions.insert().values(**values)
        item.id = await self.database.execute(query)
        return item

    async def get_session_by_user_id(self, user_id) -> List[Session]:
        query = sessions.select().where(sessions.c.user_id == user_id)
        items = await self.database.fetch_all(query)
        if items is None or not items:
            return []
        sessions_list = []
        for i in items:
            session = Session.parse_obj(i)
            sessions_list.append(session)
        return sessions_list

    async def get_last_session(self, user_id) -> Optional[Session]:
        query = sessions.select().where(sessions.c.user_id == user_id).order_by(sessions.c.id.desc())
        item = await self.database.fetch_one(query)
        if item is None:
            return None
        session = Session.parse_obj(item)
        return session

    async def set_finish(self, session: Session):
        now = datetime.utcnow()
        session.finished_at = now
        query = sessions.update().where(sessions.c.id == session.id)
        values = {**session.dict()}
        await self.database.execute(query, values=values)
        return session
