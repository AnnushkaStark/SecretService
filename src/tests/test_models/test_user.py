from sqlalchemy.ext.asyncio import AsyncSession

from models import User


class TestUserModel:
    async def test_fields(self, async_session: AsyncSession) -> None:
        current_fields_name = [i.name for i in User.__table__.columns]
        related_fields = [
            i._dependency_processor.key for i in User.__mapper__.relationships
        ]
        all_model_fields = current_fields_name + related_fields
        schema_fields_name = {
            "username",
            "email",
            "password",
            "secrets",
        }
        for field in schema_fields_name:
            assert field in all_model_fields, (
                "Нет необходимого поля %s" % field
            )
