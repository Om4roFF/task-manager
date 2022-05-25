from .base import metadata, engine
from .users import users
from .auth import auth
from .cities import cities
from .comments import comments
from .boards import boards
from .groups import groups
from .task import tasks
from .company import companies
from .user_group import user_group_table
from .sessions import sessions
from .admins import admins
metadata.create_all(bind=engine)
