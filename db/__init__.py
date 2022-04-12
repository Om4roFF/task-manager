from .base import metadata, engine
from .users import users
from .auth import auth
from .cities import cities
# from .comments import comments
from .boards import boards
from .groups import groups
from .task import tasks
from .company import companies
metadata.create_all(bind=engine)
