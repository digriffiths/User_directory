from .routers.router import router as my_router
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import logging
from .services.LoggingMiddleware import LoggingMiddleware

app = FastAPI()

app.add_middleware(LoggingMiddleware)

app.include_router(my_router)
