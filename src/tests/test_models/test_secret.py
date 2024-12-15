from sqlalchemy.ext.asyncio import AsyncSession

from models import Secret


class TestSecretModel:
    async def test_fields(self, async_session: AsyncSession) -> None:
        current_fields_name = [i.name for i in Secret.__table__.columns]
        related_fields = [
            i._dependency_processor.key
            for i in Secret.__mapper__.relationships
        ]
        all_model_fields = current_fields_name + related_fields
        schema_fields_name = {
            "name",
            "secret",
            "key",
            "created_at",
            "owner_id",
            "owner",
        }
        for field in schema_fields_name:
            assert field in all_model_fields, (
                "Нет необходимого поля %s" % field
            )
