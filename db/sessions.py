import sqlalchemy
from .base import metadata

sessions = sqlalchemy.Table(
    "session",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column("latitude", sqlalchemy.Float),
    sqlalchemy.Column("longitude ", sqlalchemy.Float),
    sqlalchemy.Column("started_at", sqlalchemy.DateTime,),
    sqlalchemy.Column("finished_at", sqlalchemy.DateTime,),
)