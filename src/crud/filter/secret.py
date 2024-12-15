from typing import Sequence

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api.filters.secret import SecretFilter
from models import Secret


async def filter_secret(
    db: AsyncSession,
    filter: SecretFilter,
    owner_id: int,
    skip: int,
    limit: int,
) -> Sequence[Secret]:
    statement = (
        select(Secret, func.count().over().label("total"))
        .offset(skip)
        .limit(limit)
        .where(Secret.owner_id == owner_id)
    )
    if filter.created_at__gte is not None:
        statement = statement.where(
            func.date(Secret.created_at) >= filter.created_at__gte
        )
    if filter.created_at__lte is not None:
        statement = statement.where(
            func.date(Secret.created_at) <= filter.created_at__lte
        )
    result = await db.execute(statement)
    rows = result.mappings().all()
    return {
        "limit": limit,
        "offset": skip * limit,
        "total": rows[0]["total"] if rows else 0,
        "objects": [r["Secret"] for r in rows],
    }
