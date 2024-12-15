from typing import Callable

from httpx import AsyncClient

from models.user import User

ROOT_ENDPOINT = "/secret_service/api/v1/user/"


class TestLogout:
    async def test_logout(
        self,
        http_client: AsyncClient,
        user_fixture: User,
        get_auth_headers: Callable,
    ) -> None:
        endpoint = f"{ROOT_ENDPOINT}logout/"
        user_auth_headers = await get_auth_headers(user_fixture)
        response = await http_client.delete(
            endpoint, headers=user_auth_headers
        )
        assert response.status_code == 200
