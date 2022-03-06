from databases import Database
from fastapi import FastAPI
from sqlalchemy.ext.declarative import declarative_base

from .config import settings
from .middlewares import setup_middlewares

app = FastAPI()
app.config = settings.settings

database = Database(app.config.database_uri)
app.database = database

db_model = declarative_base()

from . import routers  # noqa
from .context import setup_context  # noqa

setup_middlewares(app)
setup_context(app)


app.include_router(routers.tasks_router, prefix="/tasks", tags=["tasks"])
