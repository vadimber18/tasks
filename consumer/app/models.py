from enum import IntEnum

from pydantic import BaseModel, Field, validator


# TODO DRY, in real life we have microservices in separated repos tho
class TaskStatus(IntEnum):
    new = 1
    processing = 2
    completed = 3
    error = 4


class Task(BaseModel):
    id: int = Field(alias="task_id")  # noqa A003
    processing_time: int

    @validator("processing_time")
    def validate_time(cls, processing_time: int):
        if processing_time == 13:
            raise ValueError("Processing time should not be 13")
        return processing_time

    class Config:
        allow_population_by_field_name = True
