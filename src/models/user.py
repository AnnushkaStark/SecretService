from typing import TYPE_CHECKING, List

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from databases.database import Base

if TYPE_CHECKING:
    from .secret import Secret


class User(Base):
    """
    Модель пользователя

    ## Attrs:
        - id: int - идентификатор
        - username: str - юзернейм
        - email: str - элаетронная почта
        - password: str - хэш пароля
        - secrets: List[Secret] - связь
            секреты созданные пользователем
    """

    __tablename__ = "user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str]
    secrets: Mapped[List["Secret"]] = relationship(
        "Secret", back_populates="owner"
    )
