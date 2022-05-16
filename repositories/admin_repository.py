import datetime

from sqlalchemy import and_

from db.admins import admins
from models.admin import Admin, AdminReg
from repositories.base import BaseRepository


class AdminRepository(BaseRepository):

    async def get_admin(self, admin: Admin):
        query = admins.select().where(
            and_(admins.c.email == admin.email))
        adm = await self.database.fetch_one(query)
        if adm is None:
            return None
        return Admin.parse_obj(adm)

    async def create(self, admin: AdminReg, company_id: int):
        from core.security import get_password_hash
        now = datetime.datetime.utcnow()
        query = admins.insert().values({'email': admin.email, 'hashed_password': get_password_hash(admin.password1),
                                        'created_at': now, 'updated_at': now, 'company_id': company_id})
        await self.database.execute(query)
        return True
