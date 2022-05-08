from sqlalchemy import and_

from db.admins import admins
from models.admin import Admin
from repositories.base import BaseRepository


class AdminRepository(BaseRepository):

    async def get_admin(self, admin: Admin):
        query = admins.select().where(
            and_(admins.c.email == admin.email, admins.c.hashed_password == admin.hashed_password))
        adm = await self.database.fetch_one(query)
        return Admin.parse_obj(adm)
