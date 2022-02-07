from repositories.user_repository import UserRepository
from db.base import database


def get_user_repository() -> UserRepository:
    return UserRepository(database)
