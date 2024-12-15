from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from api.filters.secret import SecretFilter
from crud.filter.secret import filter_secret
from crud.secret import secret_crud
from models import Secret
from schemas.secret import (
    SecretCreate,
    SecretCreateDB,
    SecretFullResponse,
    SecretPaginatedResponse,
)
from utilities.secret import decrypt_data, encrypt_data


async def create(
    db: AsyncSession, create_data: SecretCreate, owner_id: int
) -> Secret:
    create_schema = SecretCreateDB(
        name=create_data.name,
        secret=await encrypt_data(data=create_data.secret),
        owner_id=owner_id,
    )
    secret = await secret_crud.create(db=db, create_schema=create_schema)
    return secret


async def read_one(db: AsyncSession, db_obj: Secret) -> SecretFullResponse:
    secret = SecretFullResponse(
        id=db_obj.id,
        name=db_obj.name,
        secret=await decrypt_data(data=db_obj.secret),
    )
    await secret_crud.mark_deleted(db=db, obj=db_obj)
    return secret


async def read_multi(
    db: AsyncSession,
    owner_id: int,
    skip: int,
    limit: int,
    filter: Optional[SecretFilter] = None,
) -> SecretPaginatedResponse:
    if filter:
        return await filter_secret(
            db=db, owner_id=owner_id, skip=skip, limit=limit
        )
    return await secret_crud.get_multi_with_total_by_owner_id(
        db=db, owner_id=owner_id, skip=skip, limit=limit
    )
