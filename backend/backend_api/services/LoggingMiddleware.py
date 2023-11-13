from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import logging


class LoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, **kwargs):
        super().__init__(app, **kwargs)
        logging.basicConfig(level=logging.INFO,
                            filename='app.log',
                            filemode='w',
                            format='%(name)s - %(levelname)s - %(message)s')

    async def dispatch(self, request: Request, call_next):
        logging.info(f"Incoming request: {request.method} {request.url}")
        response = await call_next(request)
        logging.info(f"Outgoing response: {response.status_code}")
        return response
