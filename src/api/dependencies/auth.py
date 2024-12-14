import os
from datetime import timedelta

from authlib.jose import JoseError
from dotenv import load_dotenv  # noqa: F401
from fastapi import Depends, HTTPException, Security
from fastapi_jwt import (
    JwtAccessBearerCookie,
    JwtAuthorizationCredentials,
    JwtRefreshBearer,
)
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from constants.jwt_settings import (
    JWT_ACCESS_TOKEN_EXPIRES,
    JWT_REFRESH_TOKEN_EXPIRES,
)
from crud.user import crud_user
from databases.database import get_async_session
from models import User
from schemas.token import TokenPayload

access_security = JwtAccessBearerCookie(
    secret_key=os.getenv("JWT_SECRET_KEY"),
    auto_error=True,
    access_expires_delta=timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRES),
)
refresh_security = JwtRefreshBearer(
    secret_key=os.getenv("JWT_REFRESH_SECRET_KEY"),
    refresh_expires_delta=timedelta(minutes=JWT_REFRESH_TOKEN_EXPIRES),
    auto_error=True,
)


async def get_current_user(
    credentials: JwtAuthorizationCredentials = Security(access_security),
    db: AsyncSession = Depends(get_async_session),
) -> User:
    if credentials is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        token_user = TokenPayload(**credentials.subject)
    except (JoseError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    return await crud_user.get_by_username(db=db, username=token_user.username)
