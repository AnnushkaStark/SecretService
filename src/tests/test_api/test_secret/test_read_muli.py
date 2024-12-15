from typing import Callable

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from models import Secret, User

ROOT_ENDPOINT = "/secret_service/api/v1/secret/"


class TestReadSecretsMulti:
    async def test_read_secrets_by_owner(
        self,
        http_client: AsyncClient,
        async_session: AsyncSession,
        user_fixture: User,
        get_auth_headers: Callable,
        secret_first_fixture: Secret,
        secret_second_fixture: Secret,
    ) -> None:
        user_auth_headers = await get_auth_headers(user_fixture)
        response = await http_client.get(
            ROOT_ENDPOINT, headers=user_auth_headers
        )
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["total"] == 2
        assert response_data["objects"][0]["name"] == secret_first_fixture.name
        assert (
            response_data["objects"][1]["name"] == secret_second_fixture.name
        )

    async def test_read_secrets_by_user_without_secrets(
        self,
        http_client: AsyncClient,
        async_session: AsyncSession,
        user_without_secrets_fixture: User,
        get_auth_headers: Callable,
        secret_first_fixture: Secret,
        secret_second_fixture: Secret,
    ) -> None:
        user_auth_headers = await get_auth_headers(
            user_without_secrets_fixture
        )
        response = await http_client.get(
            ROOT_ENDPOINT, headers=user_auth_headers
        )
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["total"] == 0
        assert response_data["objects"] == []
