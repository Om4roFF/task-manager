from .base import metadata, engine
from .users import users

metadata.create_all(bind=engine)
