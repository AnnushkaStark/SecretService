from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.secret import SecretPaginatedResponse
from utilities.search import get_transliterated_value
from models import Secret


class SearchSecretCRUD:
    async def get_search_secret_crud_result(
        self,
        db: AsyncSession,
        owner_id: int,
        query: str,
        skip: int = 0,
        limit: int = 10,
    ) -> SecretPaginatedResponse:
        kwargs = {
            "db": db,
            "owner_id": owner_id,
            "query": await get_transliterated_value(query=query),
            "skip": skip,
            "limit": limit,
        }
        result = await self.get_search_result(**kwargs)
        return result
    
    async def get_search_result(
        self,
        db: AsyncSession,
        owner_id: int,
        query: list[str],
        skip: int = 0,
        limit: int = 10,
    ) -> Sequence[Secret]:
        statement = (
            select(Secret)
            .filter(
                Secret.owner_id==owner_id,
                Secret.is_active.is_(True),
                *(Secret.name.ilike(f"%{q}%") for q in query),    
            )
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(statement)
        rows = result.mappings().unique().all()
        return {
            "limit": limit,
            "offset": skip * limit,
            "total": rows[0]["total"] if rows else 0,
            "objects": [r["Secret"] for r in rows],
        }
