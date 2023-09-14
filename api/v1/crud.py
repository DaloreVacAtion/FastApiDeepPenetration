from sqlalchemy import select, update, text, delete
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User
from auth.schemas import UserUpdate, UserRead


async def delete_user(user: User, session: AsyncSession):
    statement = (
        delete(User).
        where(User.id == user.id)
    )
    await session.execute(statement)
    await session.commit()


async def update_user(user: User, user_in: UserUpdate, session: AsyncSession) -> UserRead:
    update_data = user_in.model_dump(exclude_unset=True)
    statement = (
        update(User).
        where(User.id == user.id).
        values(**update_data)
    )
    await session.execute(statement)
    await session.commit()
    await session.refresh(user)
    return user
