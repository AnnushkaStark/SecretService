from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi_filter import FilterDepends
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies.auth import get_current_user
from api.dependencies.database import get_async_db
from api.filters.secret import SecretFilter
from crud.secret import secret_crud
from models import User
from schemas.secret import (
    SecretCreate,
    SecretFullResponse,
    SecretPaginatedResponse,
)
from services import secret as secret_service

router = APIRouter()


@router.get("/", response_model=SecretPaginatedResponse)
async def read_secrets(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
    filter: SecretFilter = FilterDepends(SecretFilter),
    limit: int = 20,
    skip: int = 0,
):
    return await secret_service.read_multi(
        db=db, owner_id=current_user.id, filter=filter, skip=skip, limit=limit
    )


@router.get("/{secret_id}/", response_model=SecretFullResponse)
async def read_secret(
    secret_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    if found_secret := await secret_crud.get_by_id_and_owner_id(
        db=db, obj_id=secret_id, owner_id=current_user.id
    ):
        return await secret_service.read_one(db=db, db_obj=found_secret)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Not found"
    )


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_secret(
    secret: SecretCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return await secret_service.create(
            db=db, create_data=secret, owner_id=current_user.id
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
