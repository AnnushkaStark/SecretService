import sys
from typing import Callable, Generator

import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from databases.database import Base, async_engine
from main import app
from models import User
from utilities.security.security import access_security

from .fixtures import *  # noqa: F403, F401

assert (sys.version_info.major, sys.version_info.minor) == (
    3,
    11,
), "Only Python 3.11 allowed"


@pytest_asyncio.fixture
async def async_session() -> AsyncSession:
    session = sessionmaker(
        async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with session() as s:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        yield s

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await async_engine.dispose()


@pytest_asyncio.fixture
async def http_client(
    async_session: AsyncSession,
) -> Generator[AsyncClient, None, None]:
    async with AsyncClient(app=app, base_url="http://0.0.0.0:8000") as ac:
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
