from typing import Callable

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from models import Secret, User

ROOT_ENDPOINT = "/secret_service/api/v1/secret/"


class TestReadSecret:
    async def test_read_secret_by_owner(
        self,
        http_client: AsyncClient,
        async_session: AsyncSession,
        user_fixture: User,
        get_auth_headers: Callable,
        secret_first_fixture: Secret,
    ) -> None:
        endpoint = f"{ROOT_ENDPOINT}{secret_first_fixture.id}/"
        user_auth_headers = await get_auth_headers(user_fixture)
        response = await http_client.get(endpoint, headers=user_auth_headers)
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["name"] == secret_first_fixture.name

    async def test_read_secret_by_another_user(
        self,
        http_client: AsyncClient,
        async_session: AsyncSession,
        user_without_secrets_fixture: User,
        get_auth_headers: Callable,
        secret_first_fixture: Secret,
    ) -> None:
        endpoint = f"{ROOT_ENDPOINT}{secret_first_fixture.id}/"
        user_auth_headers = await get_auth_headers(
            user_without_secrets_fixture
        )
        response = await http_client.get(endpoint, headers=user_auth_headers)
        assert response.status_code == 404
        response_data = response.json()
        assert response_data["detail"] == "Not found"

    async def test_read_secret_with_invalid_id(
        self,
        http_client: AsyncClient,
        async_session: AsyncSession,
        user_fixture: User,
        get_auth_headers: Callable,
        secret_first_fixture: Secret,
    ) -> None:
        endpoint = f"{ROOT_ENDPOINT}121313/"
        user_auth_headers = await get_auth_headers(user_fixture)
        response = await http_client.get(endpoint, headers=user_auth_headers)
        assert response.status_code == 404
        response_data = response.json()
        assert response_data["detail"] == "Not found"
