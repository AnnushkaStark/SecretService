from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from databases.database import Base

if TYPE_CHECKING:
    from .user import User


class Secret(Base):
    """
    Модель секрета

    ## Attrs:
        - id: int - идентификатор
        - name: str - название
        - secret: str - зашифрованные
            данные
        - owner_id: int - идентификатор
            пользователя который создал секрет
            FK User
        - owner: User - связь пользователь
            который создал секрет
    """

    __tablename__ = "secret"
    __table_args__ = (
        UniqueConstraint("name", "owner_id", name="uix_secret_name"),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True)
    secret: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    owner_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user.id", ondelete="CASCADE")
    )
    owner: Mapped["User"] = relationship("User", back_populates="secrets")
