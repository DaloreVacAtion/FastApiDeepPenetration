from httpx import AsyncClient
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from auth.models import User
from services.users import pwd_context
from tests.factories import UserModelFactory


async def get_user_token(ac: AsyncClient, username: str, password: str) -> str | None:
    auth = await ac.post('api/v1/users/auth/token', data={
        'username': username,
        'password': password,
    })
    token = auth.json().get('access_token') if auth.status_code == status.HTTP_200_OK else None
    return token


async def get_user_by_id(user_id: int, session: AsyncSession) -> User | None:
    users = await session.execute(select(User).where(User.id == user_id))
    user = users.scalars().first()
    return user


async def create_user(
    session: AsyncSession,
    **kwargs,
):
    password = kwargs.pop('password')
    hashed_password = pwd_context.hash(password)
    user = UserModelFactory(
        age=20,
        hashed_password=hashed_password,
        is_active=True,
        is_superuser=kwargs.pop('superuser', False),
        is_verified=True,
        **kwargs,
    )
    await session.commit()
    return user


async def clear_users(
    session: AsyncSession,
):
    statement = text(f'delete from public.user')
    await session.execute(statement)
    await session.commit()
