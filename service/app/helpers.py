import json

import aio_pika


async def publish_message(app, message):
    await app.broker_channel.default_exchange.publish(
        aio_pika.Message(body=json.dumps(message).encode()),
        routing_key=app.config.broker_routing_key,
    )
