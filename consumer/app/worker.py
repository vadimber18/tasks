import time
import json
import asyncio

import httpx
from celery import Celery
from celery.signals import celeryd_init

from app import app
from .models import TaskStatus, Task
from .logger import get_logger
from .helpers import process_request_async, process_request


celery = Celery(__name__)
celery.conf.broker_url = app.config.broker_uri
celery.conf.result_backend = app.config.result_backend


def celery_setup_context():
    """Celery app does not launch fastapi server itself."""
    if not hasattr(app, "logger"):
        app.logger = get_logger()
    if not hasattr(app, "client"):
        app.client = httpx.Client()


@celeryd_init.connect
def configure_workers(sender=None, conf=None, **kwargs):
    celery_setup_context()


@celery.task(name="process_task")
def process_task(message: dict):
    """Process default cpu-bound task."""
    update_status_url = f"{app.config.tasks_api_uri}/{message['id']}"
    try:
        task = Task(**message)
        process_request(
            method="patch",
            url=update_status_url,
            json={"status": TaskStatus.processing},
        )
        time.sleep(task.processing_time)
        process_request(
            method="patch",
            url=update_status_url,
            json={"status": TaskStatus.completed},
        )
    except Exception as e:
        app.logger.exception(e)
        process_request(
            method="patch",
            url=update_status_url,
            json={"status": TaskStatus.error},
        )


async def process_io_task(message: dict):
    """Process task asynchronously."""
    update_status_url = f"{app.config.tasks_api_uri}/{message['id']}"
    try:
        task = Task(**message)
        await process_request_async(
            method="patch",
            url=update_status_url,
            json={"status": TaskStatus.processing},
        )
        await asyncio.sleep(task.processing_time)
        await process_request_async(
            method="patch",
            url=update_status_url,
            json={"status": TaskStatus.completed},
        )
    except Exception as e:
        app.logger.exception(e)
        await process_request_async(
            method="patch",
            url=update_status_url,
            json={"status": TaskStatus.error},
        )


async def process_incoming_message(message):
    await message.ack()
    body = json.loads(message.body)
    app.logger.info(f"received message {body}")
    if body.get("cpu_bound"):
        process_task.delay(body)
    else:
        asyncio.create_task(process_io_task(body))
