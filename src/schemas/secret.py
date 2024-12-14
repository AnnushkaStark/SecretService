from typing import List

from pydantic import BaseModel, Field

from constants.secret import (
    MAX_SECRET_LENGTH,
    MAX_SECRET_NAME_LENGTH,
    MIN_SECRET_LENGTH,
    MIN_SECRET_NAME_LENGTH,
)
from schemas.paginate import PaginatedResponseBase


class SecretBase(BaseModel):
    class Config:
        from_attributes = True


class SecretCreate(SecretBase):
    name: str = Field(
        min_length=MIN_SECRET_NAME_LENGTH, max_length=MAX_SECRET_NAME_LENGTH
    )
    secret: str = Field(
        min_length=MIN_SECRET_LENGTH, max_length=MAX_SECRET_LENGTH
    )


class SecretCreateDB(SecretCreate):
    secret: bytes
    owner_id: int

    class Config:
        from_attributes = True


class SecretResponse(SecretBase):
    id: int
    name: str


class SecretFullResponse(SecretCreate):
    id: int


class SecretPaginatedResponse(PaginatedResponseBase):
    objects: List[SecretResponse] = []
