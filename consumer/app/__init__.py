from fastapi import FastAPI

from .config import settings


app = FastAPI()
app.config = settings.settings

from .context import setup_context # noqa

setup_context(app)
