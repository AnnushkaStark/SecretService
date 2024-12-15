from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from crud.user import user_crud
from models import User
from schemas.user import UserCreate

ROOT_ENDPOINT = "/secret_service/api/v1/user/"


class TestCreateUser:
    async def test_create(
        self, http_client: AsyncClient, async_session: AsyncSession
    ) -> None:
        data = UserCreate(
            username="Vasya",
            email="ThisIsMyMail@gmail.com",
            password="12345678",
            password_confirm="12345678",
        )
        response = await http_client.post(
            ROOT_ENDPOINT, json=data.model_dump()
        )
        assert response.status_code == 201
        await async_session.close()
        response_data = response.json()
        assert response_data["username"] == data.username
        new_user = await user_crud.get_by_username(
            db=async_session, username=data.username
        )
        assert new_user is not None
        assert new_user.username == data.username

    async def test_create_user_duplicate_username(
        self,
        http_client: AsyncClient,
        async_session: AsyncSession,
        user_fixture: User,
    ) -> None:
        data = UserCreate(
            username=user_fixture.username,
            email="mytestmai_4l@gmail.com",
            password="12345678",
            password_confirm="12345678",
        )
        response = await http_client.post(
            ROOT_ENDPOINT, json=data.model_dump()
        )
        assert response.status_code == 400
        await async_session.close()
        response_data = response.json()
        assert response_data["detail"] == "Username alredy exsists!"
        not_created_user = await user_crud.get_by_email(
            db=async_session, email=data.email
        )
        assert not_created_user is None

    async def test_create_user_duplicate_email(
        self,
        http_client: AsyncClient,
        async_session: AsyncSession,
        user_fixture: User,
    ) -> None:
        data = UserCreate(
            username="Mashka",
            email=user_fixture.email,
            password="12345678",
            password_confirm="12345678",
        )
        response = await http_client.post(
            ROOT_ENDPOINT, json=data.model_dump()
        )
        assert response.status_code == 400
        await async_session.close()
        response_data = response.json()
        assert response_data["detail"] == "Email alredy exsists!"
        not_created_user = await user_crud.get_by_username(
            db=async_session, username=data.username
        )
        assert not_created_user is None

    async def test_create_with_invalid_passsword_confirm(
        self, http_client: AsyncClient, async_session: AsyncSession
    ) -> None:
        data = UserCreate(
            username="Testusernew",
            email="mytestmail_5@mail.ru",
            password="12345678",
            password_confirm="123456789",
        )
        response = await http_client.post(
            ROOT_ENDPOINT, json=data.model_dump()
        )
        assert response.status_code == 400
        await async_session.close()
        response_data = response.json()
        assert response_data["detail"] == "Passwords don`t match!"
        not_created_user = await user_crud.get_by_username(
            db=async_session, username=data.username
        )
        assert not_created_user is None
