from repositories.auth_repository import AuthRepository
from repositories.user_repository import UserRepository
from db.base import database


def get_user_repository() -> UserRepository:
    return UserRepository(database)


def get_auth_repository() -> AuthRepository:
    return AuthRepository(database)
