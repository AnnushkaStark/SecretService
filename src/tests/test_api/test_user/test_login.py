from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User

ROOT_ENDPOINT = "/secret_service/api/v1/user/"


class TestLogin:
    async def test_login_succsess(
        self,
        http_client: AsyncClient,
        async_session: AsyncSession,
        user_fixture: User,
    ) -> None:
        data = {"username": user_fixture.username, "password": "123456789"}
        response = await http_client.post(f"{ROOT_ENDPOINT}login/", json=data)
        assert response.status_code == 200
        tokens = response.json()
        assert "access_token" in tokens
        assert "refresh_token" in tokens
        assert tokens["token_type"] == "bearer"
        data = {"username": "testuser", "password": "qwerty"}
        refresh_token = tokens["refresh_token"]
        headers = {"Authorization": f"Bearer {refresh_token}"}
        response = await http_client.post(
            ROOT_ENDPOINT + "refresh/", json=data, headers=headers
        )
        assert response.status_code == 200
        tokens = response.json()
        assert "access_token" in tokens
        assert "refresh_token" in tokens
        assert tokens["token_type"] == "bearer"

    async def test_login_with_invalid_username(
        self,
        http_client: AsyncClient,
        async_session: AsyncSession,
        user_fixture: User,
    ) -> None:
        data = {"username": "бла бла бла", "password": "123456789"}
        response = await http_client.post(f"{ROOT_ENDPOINT}login/", json=data)
        assert response.status_code == 404
        response_data = response.json()
        assert response_data["detail"] == "Not found"

    async def test_login_with_invalid_password(
        self,
        http_client: AsyncClient,
        async_session: AsyncSession,
        user_fixture: User,
    ) -> None:
        data = {"username": user_fixture.username, "password": "1121312323"}
        response = await http_client.post(f"{ROOT_ENDPOINT}login/", json=data)
        assert response.status_code == 400
        response_data = response.json()
        assert response_data["detail"] == "User password is wrong!"
