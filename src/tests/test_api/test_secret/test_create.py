from typing import Callable

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from models import  User
from schemas.secret import SecretCreate

ROOT_ENDPOINT = "/secret_service/api/v1/secret/"


class TestSecretCreate:
    async def test_create(
        self,
        http_client: AsyncClient,
        async_session: AsyncSession,
        user_fixture: User,
        get_auth_headers: Callable,
    ) -> None:
        user_auth_headers = await get_auth_headers(user_fixture)
        data = SecretCreate(
            name="Vasya",
            secret="ThisIsMyMail@gmail.com",
        )
        response = await http_client.post(
            ROOT_ENDPOINT, json=data.model_dump(), headers=user_auth_headers
        )
        assert response.status_code == 201
        response_data = response.json()
        assert response_data["name"] == data.name
