from db_model import Tasks as _Tasks
from .base import Base


class Tasks(Base):
    ilike_fields = ("name",)
    exact_fields = ("id", "status")

    table = _Tasks.__table__

    def __init__(self, database):
        super().__init__(database)
