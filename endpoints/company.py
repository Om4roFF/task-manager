from fastapi import APIRouter, Depends, HTTPException

from endpoints.depends import get_company_repository
from repositories.company_repository import CompanyRepository

router = APIRouter()


@router.get('/')
async def get_companies(company_code: str, company_repository: CompanyRepository = Depends(get_company_repository)):
    company_code = company_code.upper()
    company = await company_repository.get_company_by_code(company_code=company_code)
    if company is None:
        raise HTTPException(status_code=400, detail='company not exist')
    return company

