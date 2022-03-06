import asyncio
from typing import List, Optional

from fastapi import APIRouter, Request, Response, Depends
from fastapi import status as _status

from app.models import (
    Task,
    RequestTaskPost,
    TaskBase,
    TaskStatus,
    RequestTaskUpdate,
    TaskFull,
)
from app.helpers import publish_message
from .common import CommonPaginationParams

router = APIRouter()


@router.get("", response_model=List[Task], summary="List tasks")
async def get_tasks(
    request: Request,
    status: Optional[TaskStatus] = None,
    name: Optional[str] = None,
    pagination: CommonPaginationParams = Depends(),
):
    tasks = await request.app.tasks.select(
        multiple=True,
        status=status,
        name=name,
        limit=pagination.limit,
        offset=pagination.offset,
    )
    return [Task(**task).dict() for task in tasks]


@router.get("/{task_id}", response_model=Task, summary="Get task by id")
async def get_task(request: Request, task_id: int):
    return await request.app.tasks.select(id=task_id) or Response(
        status_code=_status.HTTP_404_NOT_FOUND
    )


@router.post(
    "",
    response_model=TaskBase,
    status_code=_status.HTTP_201_CREATED,
    summary="Create task",
)
async def post_task(request: Request, task: RequestTaskPost):
    created = await request.app.tasks.insert(**task.dict())
    asyncio.create_task(
        publish_message(request.app, TaskFull(id=created["id"], **task.dict()).dict())
    )
    return created


@router.patch(
    "/{task_id}",
    response_model=None,
    status_code=_status.HTTP_204_NO_CONTENT,
    summary="Update task status",
)
async def update_task_status(request: Request, task_id: int, task: RequestTaskUpdate):
    await request.app.tasks.update({"id": task_id}, {"status": task.status})
    return Response(status_code=_status.HTTP_204_NO_CONTENT)
