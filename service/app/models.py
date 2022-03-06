from enum import IntEnum
from typing import Optional

from pydantic import BaseModel, Field


class TaskStatus(IntEnum):
    new = 1
    processing = 2
    completed = 3
    error = 4


class RequestTaskPost(BaseModel):
    name: str
    processing_time: int
    status: Optional[TaskStatus] = TaskStatus.new
    cpu_bound: Optional[bool] = True


class RequestTaskUpdate(BaseModel):
    status: TaskStatus

    class Config:
        allow_population_by_field_name = True


class TaskBase(BaseModel):
    id: int = Field(alias="task_id")  # noqa A003

    class Config:
        allow_population_by_field_name = True


class Task(TaskBase):
    name: str
    processing_time: int
    status: TaskStatus = TaskStatus.new


class TaskFull(Task):
    cpu_bound: Optional[bool] = True
