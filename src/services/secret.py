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
    SecretResponse,
)
from utilities.secret import decrypt_data, encrypt_data, get_secret_key


async def create(
    db: AsyncSession, create_data: SecretCreate, owner_id: int
) -> SecretResponse:
    key = await get_secret_key()
    create_schema = SecretCreateDB(
        name=create_data.name,
        key=key,
        secret=await encrypt_data(data=create_data.secret, key=key),
        owner_id=owner_id,
    )
    try:
        secret = await secret_crud.create(db=db, create_schema=create_schema)
    except Exception as e:
        raise Exception(str(e))
    visible_secret = SecretResponse(
        id=secret.id, name=secret.name, created_at=secret.created_at
    )
    return visible_secret


async def read_one(db: AsyncSession, db_obj: Secret) -> SecretFullResponse:
    secret = SecretFullResponse(
        id=db_obj.id,
        name=db_obj.name,
        secret=await decrypt_data(data=db_obj.secret, key=db_obj.key),
    )
    await secret_crud.remove(db=db, obj_id=db_obj.id)
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
            db=db, owner_id=owner_id, skip=skip, limit=limit, filter=filter
        )
    return await secret_crud.get_multi_with_total_by_owner_id(
        db=db, owner_id=owner_id, skip=skip, limit=limit
    )
