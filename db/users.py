import sqlalchemy
from .base import metadata
import datetime

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("phone", sqlalchemy.String, primary_key=True, unique=True),
    sqlalchemy.Column("role", sqlalchemy.String),
    sqlalchemy.Column("position", sqlalchemy.String),
    sqlalchemy.Column("total_money_in_kzt", sqlalchemy.Integer),
    sqlalchemy.Column("image_url", sqlalchemy.String),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, default=datetime.datetime.utcnow),
    sqlalchemy.Column("last_visit_time", sqlalchemy.DateTime, default=datetime.datetime.utcnow),
    sqlalchemy.Column("updated_at", sqlalchemy.DateTime, default=datetime.datetime.utcnow)
)
