
import sqlalchemy
from .base import metadata
import datetime

user_group_table = sqlalchemy.Table(
    "user_group",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("group_id", sqlalchemy.ForeignKey('groups.id')),
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey('users.id')),
)
