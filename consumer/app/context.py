import asyncio

import aio_pika
import httpx

from .worker import process_incoming_message
from .logger import get_logger


def setup_context(app):
    setup_logger(app)
    setup_client(app)
    setup_broker(app)


def setup_logger(app):
    @app.on_event("startup")
    def startup_logger():
        app.logger = get_logger()


def setup_client(app):
    @app.on_event("startup")
    async def startup_client():
        app.async_client = httpx.AsyncClient()
        app.client = httpx.Client()

    @app.on_event("shutdown")
    async def shutdown_client():
        app.client.close()
        await app.async_client.aclose()


def setup_broker(app):
    @app.on_event("startup")
    async def startup_broker():
        if rabbitmq_uri := app.config.rabbitmq_uri:
            retries = 0
            while (
                not hasattr(app, "broker") and retries < app.config.rabbitmq_max_retries
            ):
                try:
                    app.broker = await aio_pika.connect_robust(rabbitmq_uri)
                    app.logger.info("connected to broker")
                except Exception:
                    retries += 1
                    app.logger.info(f"trying to connect to broker {retries}/100")
                    await asyncio.sleep(3)
            if retries > app.config.rabbitmq_max_retries:
                app.logger.info("failed to connect to broker")
                return
            app.broker_channel = await app.broker.channel()
            queue = await app.broker_channel.declare_queue(
                app.config.broker_routing_key
            )
            await queue.consume(process_incoming_message, no_ack=False)
