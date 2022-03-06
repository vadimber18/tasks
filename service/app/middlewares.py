import time

from fastapi import Request, status
from fastapi.responses import Response


def setup_middlewares(app):
    app.middleware("http")(exception_handler)
    app.middleware("http")(log_request)


EXCLUDE_PATH = ("openapi.json", "docs")


async def log_request(request: Request, call_next):
    url = str(request.url)
    path = url[len(str(request.base_url)):]  # noqa BLK100
    if any((path.startswith(each) for each in EXCLUDE_PATH)):
        return await call_next(request)

    # TODO cant do request.json() here because of fastapi drain
    json_payload = None
    log_extra = {
        "method": request.method,
        "headers": request.headers,
        "json": json_payload,
        "query": request.query_params,
        "path": request.path_params,
        "url": url,
        "handler": "unknown",
    }
    start_time = time.time()
    try:
        response = await call_next(request)
        # endpoint appears after handler is done
        if "endpoint" in request.scope:
            handler_name = request.scope["endpoint"].__name__
            log_extra["handler"] = handler_name
        log_extra["processed_time"] = time.time() - start_time
        request.app.logger.info("request done", extra=log_extra)
        return response
    except Exception:
        if "endpoint" in request.scope:
            handler_name = request.scope["endpoint"].__name__
            log_extra["handler"] = handler_name
        log_extra["processed_time"] = time.time() - start_time
        request.app.logger.info("exception occurred", extra=log_extra)
        raise


async def exception_handler(request: Request, call_next):
    try:
        response = await call_next(request)
    except Exception:
        request.app.logger.exception("Exception handler traceback")
        response = Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return response
