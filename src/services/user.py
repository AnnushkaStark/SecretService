from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from crud.user import user_crud
from models import User
from schemas.user import UserCreate, UserCreateDB, UserLogin
from utilities.security.password_hasher import (
    get_password_hash,
    verify_password,
)
from utilities.security.security import TokenSubject, create_tokens


async def create(
    db: AsyncSession, create_schema: UserCreate
) -> Optional[User]:
    if exsisted_username := await user_crud.get_by_username(  # noqa: F841
        db=db, username=create_schema.username
    ):
        raise Exception("Username alredy exsists!")
    
    if exsisted_email := await user_crud.get_by_email(  # noqa: F841
        db=db, email=create_schema.email
    ):
        raise Exception("Email alredy exsists!")
    if create_schema.password != create_schema.password_confirm:
        raise Exception("Passwords don`t match!")
    create_schema.password = get_password_hash(create_schema.password)
    del create_schema.password_confirm
    create_data = UserCreateDB(**create_schema.model_dump(exclude_unset=True))
    user = await user_crud.create(db=db, create_schema=create_data)
    return user


async def login(login_data: UserLogin, db_obj: User) -> User:
    if verify_password(
        plain_password=login_data.password,
        hashed_password=db_obj.password,
    ):
        subject = TokenSubject(
            username=str(db_obj.username),
            password=db_obj.password,
        )
        return await create_tokens(subject)
    raise Exception("User password is wrong!")
