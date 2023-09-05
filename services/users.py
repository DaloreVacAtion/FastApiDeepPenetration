from httpx import AsyncClient
from passlib.context import CryptContext
from sqlalchemy import text, insert
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from auth.models import User


async def get_user_by_id(user_id: int, session: AsyncSession) -> User | None:
    query = text(f'select * from public.user where public.user.id = {user_id}')
    user = await session.execute(query)
    return user.first()


async def get_user_by_username(username: str, session: AsyncSession) -> User | None:
    query = text(f'select * from public.user where public.user.username = \'{username}\'')
    user = await session.execute(query)
    return user.first()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_user_cookies(ac: AsyncClient, email: str, password: str) -> str | None:
    auth = await ac.post('api/v1/auth/login', data={
        "username": email,
        "password": password,
    })
    cookie = auth.cookies.get('IDP') if auth.status_code == status.HTTP_204_NO_CONTENT else None
    return cookie


async def create_user(
    session: AsyncSession,
    username: str,
    email: str,
    password: str,
    superuser: bool | None = None
):
    hashed_password = pwd_context.hash(password)
    statement = insert(User).values(
        username=username,
        email=email,
        age=15,
        hashed_password=hashed_password,
        is_active=True,
        is_superuser=superuser if superuser else False,
        is_verified=True,
    )
    await session.execute(statement)
    await session.commit()
    query = text(f'select * from public.user where public.user.email = \'{email}\'')
    user = await session.execute(query)
    return user.first().id


async def clear_users(
    session: AsyncSession,
):
    statement = text(f'delete from public.user')
    await session.execute(statement)
    await session.commit()

