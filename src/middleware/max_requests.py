import time
from collections import defaultdict
from typing import Callable

from fastapi import FastAPI, HTTPException, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(
        self, app: FastAPI, max_requests: int, per_seconds: int
    ) -> None:
        super().__init__(app)
        self.max_requests = max_requests
        self.per_seconds = per_seconds
        self.clients = defaultdict(list)

    async def dispatch(
        self, request: Request, call_next: Callable
    ) -> Response:
        client_ip = request.client.host
        current_time = time.time()
        self.clients[client_ip] = [
            timestamp
            for timestamp in self.clients[client_ip]
            if current_time - timestamp < self.per_seconds
        ]
        if len(self.clients[client_ip]) >= self.max_requests:
            raise HTTPException(status_code=429, detail="Too Many Requests")
        self.clients[client_ip].append(current_time)
        response = await call_next(request)
        return response
