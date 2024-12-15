from datetime import datetime, timedelta
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


class RateLimiterMiddleware(BaseHTTPMiddleware):
    rate_limit_duration = timedelta(minutes=60)
    rate_limit_requests = 600

    def __init__(self, app):
        super().__init__(app)
        self.request_counts = {}
        
    def dispatch(self, request, call_next):
        client_ip = request.client.host
        request_count, last_request = self.request_counts.get(client_ip, (0, datetime.min))
        elapsed_time = datetime.now() - last_request
        if elapsed_time > self.rate_limit_duration:
            request_count = 1
        else:
            if request_count >= self.rate_limit_requests:
                return JSONResponse(status_code=429, content={"message":"Rate limit exceeded"})
            request_count +=1
        self.request_counts[client_ip] = (request_count, datetime.now())
        response = call_next(request)
        return response
                