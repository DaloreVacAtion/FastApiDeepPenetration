from typing import Optional

from fastapi_users import schemas
from pydantic import BaseModel, Field


class UserCreate(schemas.BaseUserCreate):
    username: str
    email: str
    password: str
    name: str | None = Field(
        default=None, title='Имя пользователя', max_length=300,
    )
    age: int | None = Field(
        default=None, title='Возраст пользователя', gt=0,
    )
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserUpdate(BaseModel):
    name: str | None = Field(
        default=None, title='Имя пользователя', max_length=300,
    )
    age: int | None = Field(
        default=None, title='Возраст пользователя', gt=0,
    )


class UserRead(BaseModel):
    id: int
    username: str
    name: str | None = None
    age: int | None = None
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        orm_mode = True
