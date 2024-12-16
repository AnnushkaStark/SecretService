from typing import Optional, Sequence

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models import Secret
from schemas.secret import SecretBase

from .async_crud import BaseAsyncCRUD


class SecretCRUD(BaseAsyncCRUD[Secret, SecretBase]):
    async def get_by_id_and_owner_id(
        self, db: AsyncSession, obj_id: int, owner_id: int
    ) -> Optional[Secret]:
        statement = select(self.model).where(
            self.model.owner_id == owner_id,
            self.model.id == obj_id,
        )
        result = await db.execute(statement)
        return result.scalars().first()

    async def get_multi_with_total_by_owner_id(
        self, db: AsyncSession, owner_id: int, skip: int = 0, limit: int = 1000
    ) -> Sequence[Secret]:
        statement = (
            select(self.model, func.count().over().label("total"))
            .offset(skip)
            .limit(limit)
            .where(self.model.owner_id == owner_id)
            .order_by(self.model.created_at.desc())
        )
        result = await db.execute(statement)
        rows = result.mappings().all()
        return {
            "limit": limit,
            "offset": skip * limit,
            "total": rows[0]["total"] if rows else 0,
            "objects": [r["Secret"] for r in rows],
        }


secret_crud = SecretCRUD(Secret)
