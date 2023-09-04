from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, HTTPException
from fastapi_users import FastAPIUsers
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import Response

from api.v1 import crud
from auth.base_config import auth_backend
from auth.manager import get_user_manager
from auth.models import User
from auth.schemas import UserRead, UserUpdate
from db.database import get_async_session
from services.users import get_user_by_id

v1_router = APIRouter(
    prefix="/users",
    tags=['Users']
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend]
)


@v1_router.get('', response_model=UserRead, dependencies=[Depends(fastapi_users.current_user())])
async def get_user_by_username(
        username: Annotated[str, Query(title='Никнейм пользователя')],
        session: AsyncSession = Depends(get_async_session),
) -> UserRead:
    """
    Получить пользователя по username.
    """
    return await get_user_by_username(username, session)


@v1_router.patch("/{user_id}", response_model=UserRead, dependencies=[Depends(fastapi_users.current_user())])
async def update_user(
        user_id: Annotated[int, Path(title='ID пользователя', ge=0)],
        user_in: UserUpdate,
        session: AsyncSession = Depends(get_async_session),
) -> UserRead:
    """Обновить пользователя."""
    user = await crud.get_user_by_id(user_id, session)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Пользователя с id {user_id} не существет",
        )
    await crud.update_user(user_id, user_in, session)
    # Как вернуть нормального пользоваетеля?
    await session.refresh(user)
    return user


@v1_router.delete("/{user_id}", dependencies=[Depends(fastapi_users.current_user(active=True, superuser=True))])
async def delete_user(
        user_id: Annotated[int, Path(title='ID пользователя', ge=0)],
        session: AsyncSession = Depends(get_async_session),
) -> Response:
    """Удалить пользователя."""
    user = await get_user_by_id(user_id, session)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Пользователя с id {user_id} не существет",
        )

    await crud.delete_user(user, session)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
