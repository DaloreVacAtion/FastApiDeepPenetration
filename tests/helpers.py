from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from auth.models import User


async def get_user_token(ac: AsyncClient, username: str, password: str) -> str | None:
    auth = await ac.post('api/v1/users/auth/token', data={
        "username": username,
        "password": password,
    })
    token = auth.json().get('access_token') if auth.status_code == status.HTTP_200_OK else None
    return token


async def get_user_by_id(user_id: int, session: AsyncSession) -> User | None:
    users = await session.execute(select(User).where(User.id == user_id))
    user = users.scalars().first()
    return user
