import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.v1.router import api_router as secret_service_router
from middleware.max_requests import RateLimiterMiddleware

app = FastAPI(
    title="SecretService",
    openapi_url="/secret_service/openapi.json",
    docs_url="/secret_service/docs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(RateLimiterMiddleware(max_requests=600, per_seconds=60))


app.include_router(secret_service_router, prefix="/secret_service")
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        reload=True,
        proxy_headers=True,
    )
