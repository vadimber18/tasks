from app import app


async def process_request_async(**kwargs):
    response = await app.async_client.request(
        method=kwargs.get("method"),
        url=kwargs.get("url"),
        json=kwargs.get("json"),
    )
    return (
        response.json() if response.status_code != 204 else None,
        response.status_code,
        response.headers,
    )


# TODO DRY dont want to spawn threads with asyncio.run_in_executor/asyncio.in_thread
def process_request(**kwargs):
    response = app.client.request(
        method=kwargs.get("method"),
        url=kwargs.get("url"),
        json=kwargs.get("json"),
    )
    return (
        response.json() if response.status_code != 204 else None,
        response.status_code,
        response.headers,
    )
