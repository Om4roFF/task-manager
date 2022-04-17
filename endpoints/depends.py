from db.base import database
from repositories.auth_repository import AuthRepository
from repositories.board_repository import BoardRepository
from repositories.company_repository import CompanyRepository
from repositories.group_repository import GroupRepository
from repositories.user_group_repository import UserGroupRepository
from repositories.user_repository import UserRepository


def get_user_repository() -> UserRepository:
    return UserRepository(database)


def get_auth_repository() -> AuthRepository:
    return AuthRepository(database)


def get_board_repository() -> BoardRepository:
    return BoardRepository(database)


def get_company_repository() -> CompanyRepository:
    return CompanyRepository(database)


def get_group_repository() -> GroupRepository:
    return GroupRepository(database)


def get_user_group_repository() -> UserGroupRepository:
    return UserGroupRepository(database)
