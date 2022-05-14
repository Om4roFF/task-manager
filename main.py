import uvicorn
from fastapi import FastAPI

from core.config import STATIC_FILES_PATH
from db.base import database
from endpoints import users, company, boards, tasks, session, admin
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Task Manager")

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(company.router, prefix="/company", tags=["company"])
app.include_router(boards.router, prefix="/boards", tags=["boards"])
app.include_router(tasks.router, prefix='/tasks', tags=["tasks"])
app.include_router(session.router, prefix='/sessions', tags=["sessions"])
app.include_router(admin.router, prefix='/admin', tags=["sessions"])


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get('/')
async def root():
    return 'hello'
