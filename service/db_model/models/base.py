from sqlalchemy import (
    Column,
    Boolean,
    Integer,
    String,
    Enum,
)

from app import db_model
from app.models import TaskStatus


class Tasks(db_model):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    processing_time = Column(Integer, nullable=False)
    status = Column(Enum(TaskStatus), nullable=False)
    cpu_bound = Column(Boolean)

    def __repr__(self):
        return f"{self.id} {self.name}"
