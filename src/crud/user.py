from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models import User
from schemas.user import UserBase

from .async_crud import BaseAsyncCRUD


class UserCRUD(BaseAsyncCRUD[User, UserBase]):
    async def get_by_username(
        self, db: AsyncSession, username: str
    ) -> Optional[User]:
        statement = select(self.model).where(self.model.username == username)
        result = await db.execute(statement)
        return result.scalars().first()

    async def get_by_email(
        self, db: AsyncSession, email: str
    ) -> Optional[User]:
        statement = select(self.model).where(self.model.username == email)
        result = await db.execute(statement)
        return result.scalars().first()


user_crud = UserCRUD(User)
