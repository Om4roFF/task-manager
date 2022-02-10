import datetime

import sqlalchemy
from .base import metadata

auth = sqlalchemy.Table(
    "auth",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("phone", sqlalchemy.String),
    sqlalchemy.Column("code", sqlalchemy.Integer),
    sqlalchemy.Column("is_used", sqlalchemy.Boolean, default=False),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, default=datetime.datetime.utcnow),
)
