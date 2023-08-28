from typing import Optional

from httpx import AsyncClient
from passlib.context import CryptContext
from sqlalchemy import text, insert
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_user_cookies(ac: AsyncClient, email: str, password: str) -> str | None:
    auth = await ac.post('api/v1/auth/login', data={
        "username": email,
        "password": password,
    })
    cookie = auth.cookies.get('IDP') if auth.status_code == 204 else None
    return cookie


async def create_user(
    session: AsyncSession,
    username: str,
    email: str,
    password: str,
    superuser: Optional[bool] = None
):
    hashed_password = pwd_context.hash(password)
    stmt = insert(User).values(
        username=username,
        email=email,
        age=15,
        hashed_password=hashed_password,
        is_active=True,
        is_superuser=superuser if superuser else False,
        is_verified=True,
    )
    await session.execute(stmt)
    await session.commit()
    query = text(f'select * from public.user where public.user.email = \'{email}\'')
    user = await session.execute(query)
    return user.first().id


async def clear_users(
    session: AsyncSession,
):
    stmt = text(f'delete from public.user')
    await session.execute(stmt)
    await session.commit()

