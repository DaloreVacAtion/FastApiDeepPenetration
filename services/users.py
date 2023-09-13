from datetime import timedelta, datetime

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from httpx import AsyncClient
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy import text, insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from auth.models import User
from auth.schemas import UserRead
from core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='api/v1/users/auth/token')


async def get_user_by_id(user_id: int, session: AsyncSession) -> User | None:
    users = await session.execute(select(User).where(User.id == user_id))
    user = users.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Пользователя с id {user_id} не существет",
        )
    return user


async def get_user_by_username(username: str, session: AsyncSession) -> UserRead | None:
    users = await session.execute(select(User).where(User.username == username))
    user: UserRead = users.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Пользователя с такими данными не существует'
        )
    return user


async def get_user_by_username_for_login(username: str, session: AsyncSession) -> UserRead | None:
    users = await session.execute(select(User).where(User.username == username))
    user: UserRead = users.scalars().first()
    return user


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
    return user.first()


async def clear_users(
    session: AsyncSession,
):
    statement = text(f'delete from public.user')
    await session.execute(statement)
    await session.commit()


async def authenticate_user(
        username: str,
        password: str,
        session: AsyncSession
):
    user = await get_user_by_username_for_login(username, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Не смогли валидировать входящие данные.'
        )
    if not pwd_context.verify(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Не смогли валидировать входящие данные.'
        )
    return user


async def create_access_token(username: str, user_id: int, expires_at: timedelta | None = None):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.utcnow() + (expires_at if expires_at else timedelta(minutes=20))
    encode.update({'exp': expires})
    return jwt.encode(encode, settings.AUTH_SECRET_KEY, algorithm='HS256')


async def get_current_user(token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, settings.AUTH_SECRET_KEY, algorithms=['HS256'])
        username: str = payload.get('sub')
        user_id: str = payload.get('id')
        expires: str = payload.get('exp')
        if username is None or user_id is None or expires is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Bad credentials',
            )

        return {'username': username, 'id': user_id}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Bad credentials',
        )
