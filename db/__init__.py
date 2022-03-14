from .base import metadata, engine
from .users import users
from .auth import auth

metadata.create_all(bind=engine)
