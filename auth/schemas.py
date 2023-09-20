from fastapi_users import schemas
from pydantic import BaseModel, Field, ConfigDict


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
    is_active: bool | None = True
    is_superuser: bool | None = False
    is_verified: bool | None = False


class UserUpdate(BaseModel):
    name: str | None = Field(
        default=None, title='Имя пользователя', max_length=300,
    )
    age: int | None = Field(
        default=None, title='Возраст пользователя', gt=0,
    )


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    name: str | None = None
    age: int | None = None
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class Token(BaseModel):
    access_token: str
    refresh_token: str
