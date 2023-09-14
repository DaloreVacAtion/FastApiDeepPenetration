from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import Response

from api.v1 import crud
from auth.schemas import UserRead, UserUpdate
from db.database import get_async_session
from services import users as user_services
from services.users import authenticate_user, create_access_token, get_current_user

v1_router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@v1_router.get('', response_model=UserRead, dependencies=[Depends(get_current_user)])
async def get_user_by_username(
        username: Annotated[str, Query(title='Никнейм пользователя')],
        session: AsyncSession = Depends(get_async_session),
) -> UserRead:
    """Получить пользователя по username."""
    return await user_services.get_user_by_username(username, session)


@v1_router.patch("/{user_id}", response_model=UserRead, dependencies=[Depends(get_current_user)])
async def update_user(
        user_id: Annotated[int, Path(title='ID пользователя', ge=0)],
        user_in: UserUpdate,
        session: AsyncSession = Depends(get_async_session),
) -> UserRead:
    """Обновить пользователя."""
    user = await user_services.get_user_by_id(user_id, session)
    user = await crud.update_user(user, user_in, session)
    return user


@v1_router.delete("/{user_id}", dependencies=[Depends(get_current_user)])
async def delete_user(
        user_id: Annotated[int, Path(title='ID пользователя', ge=0)],
        session: AsyncSession = Depends(get_async_session),
) -> Response:
    """Удалить пользователя."""
    user = await user_services.get_user_by_id(user_id, session)
    await crud.delete_user(user, session)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@v1_router.post('/auth/token')
async def login_user_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_async_session),
):
    user = await authenticate_user(form_data.username, form_data.password, session)
    token = await create_access_token(user.username, user.id)
    return {'access_token': token, 'token_type': 'bearer'}
