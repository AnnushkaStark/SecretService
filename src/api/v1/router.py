from fastapi import APIRouter

from api.v1.enpdoints.secret import router as secret_router
from api.v1.enpdoints.user import router as user_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(user_router, prefix="/user", tags=["User"])
api_router.include_router(secret_router, prefix="/secret", tags=["Secret"])
