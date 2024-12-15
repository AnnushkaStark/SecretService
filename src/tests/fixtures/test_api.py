import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from models import Secret, User
from utilities.secret import encrypt_data, get_secret_key
from utilities.security.password_hasher import get_password_hash


@pytest_asyncio.fixture
async def user_fixture(async_session: AsyncSession) -> User:
    user = User(
        username="TestUserFirst",
        email="test_mail_1@gamil.com",
        password=get_password_hash("123456789"),
    )
    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)
    return user


@pytest_asyncio.fixture
async def user_without_secrets_fixture(async_session: AsyncSession) -> User:
    user = User(
        username="TestUserSecond",
        email="test_mail_2@gamil.com",
        password=get_password_hash("123456789"),
    )
    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)
    return user


@pytest_asyncio.fixture
async def secret_first_fixture(
    async_session: AsyncSession, user_fixture: User
) -> Secret:
    secret = Secret(
        name="my secret",
        key=await get_secret_key(),
        secret=await encrypt_data(data="big big secret"),
        owner_id=user_fixture.id,
    )
    async_session.add(secret)
    await async_session.commit()
    await async_session.refresh(secret)
    return secret


@pytest_asyncio.fixture
async def secret_second_fixture(
    async_session: AsyncSession, user_fixture: User
) -> Secret:
    secret = Secret(
        name="my secret another",
        key=await get_secret_key(),
        secret=await encrypt_data(data="big big secret"),
        owner_id=user_fixture.id,
    )
    async_session.add(secret)
    await async_session.commit()
    await async_session.refresh(secret)
    return secret
