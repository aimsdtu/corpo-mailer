from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, Response

class RateLimitMiddleware(BaseHTTPMiddleware):
    ...