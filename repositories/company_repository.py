from typing import Optional

from db import companies
from models.company import Company
from repositories.base import BaseRepository


class CompanyRepository(BaseRepository):

    async def create(self, company: Company) -> Company:
        item = Company(code=company.code)
        values = {**item.dict()}
        values.pop("id", None)
        query = companies.insert().values(**values)
        print(values)
        item.id = await self.database.execute(query)
        return item

    async def update(self, company: Company) -> Optional[Company]:
        item = Company(code=company.code, id=company.id)
        if item.id is None:
            return None
        query = companies.update().where(companies.c.id == company.id)
        values = {**item.dict()}
        values.pop("created_at", None)
        values.pop("id", None)
        await self.database.execute(query, values=values)
        return item

    async def delete(self, company_id: int) -> bool:
        try:
            query = companies.delete().where(companies.c.id == company_id)
            await self.database.execute(query)
            return True
        except:
            return False

    async def get_company_by_id(self, company_id: int):
        query = companies.select().where(companies.c.id == company_id)
        company = await self.database.fetch_one(query)
        if company is None:
            return None
        return Company.parse_obj(company)

    async def get_company_by_code(self, company_code: str):
        query = companies.select().where(companies.c.code == company_code)
        company = await self.database.fetch_one(query)
        if company is None:
            return None
        return Company.parse_obj(company)
