from typing import Callable, Generator

import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from databases.database import Base
from main import app
from models import *  # noqa: F401, F403
from utilities.security.security import access_security

from .fixtures import *  # noqa: F401, F403

TEST_DATABASE_URL = "sqlite+aiosqlite:///./secret.db"

engine_test = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)

async_session_maker = sessionmaker(
    engine_test, class_=AsyncSession, expire_on_commit=False
)


@pytest_asyncio.fixture
async def async_session() -> AsyncSession:
    session = sessionmaker(
        engine_test,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with session() as s:
        async with engine_test.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        yield s

    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine_test.dispose()


@pytest_asyncio.fixture
async def http_client(
    async_session: AsyncSession,
) -> Generator[AsyncClient, None, None]:
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000/") as ac:
        yield ac


@pytest_asyncio.fixture
async def get_auth_headers() -> Callable:
    async def _get_auth_headers(user_fixture: User):
        subject = {
            "username": user_fixture.username,
            "password": user_fixture.password,
        }
        access_token = access_security.create_access_token(subject=subject)
        headers = {"Authorization": f"Bearer {access_token}"}
        return headers

    return _get_auth_headers
