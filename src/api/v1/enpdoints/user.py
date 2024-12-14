from fastapi import APIRouter, Depends, HTTPException, Security, status
from fastapi_jwt import JwtAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

from api.dependencies.auth import refresh_security
from api.dependencies.database import get_async_db
from crud.user import user_crud
from schemas.token import TokenAccessRefresh
from schemas.user import UserCreate, UserLogin
from services import user as user_service
from utilities.security.security import (
    ACCESS_TOKEN_COOKIE_KEY,
    REFRESH_TOKEN_COOKIE_KEY,
    access_security,
    create_tokens,
)

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate, db: AsyncSession = Depends(get_async_db)
):
    try:
        return await user_service.create(db=db, create_schema=user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


@router.post("/login/", status_code=status.HTTP_200_OK)
async def login(
    login_data: UserLogin, db: AsyncSession = Depends(get_async_db)
):
    if found_user := await user_crud.get_by_username(
        db=db, username=login_data.username
    ):
        return await user_service.login(
            db_obj=found_user, login_data=login_data
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Not found"
    )


@router.post("/refresh/", response_model=TokenAccessRefresh)
async def refresh(
    credentials: JwtAuthorizationCredentials = Security(refresh_security),
):
    return await create_tokens(credentials.subject)


@router.delete("/logout/", status_code=status.HTTP_200_OK)
async def logout(
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    response = Response()
    response.delete_cookie(ACCESS_TOKEN_COOKIE_KEY)
    response.delete_cookie(REFRESH_TOKEN_COOKIE_KEY)
    return response
