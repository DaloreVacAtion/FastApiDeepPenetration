from sqlalchemy import select, update, text
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User
from auth.schemas import UserUpdate


async def delete_user(user: User, session: AsyncSession):
    stmt = text(f'delete from public.user where public.user.id = {user.id}')
    await session.execute(stmt)
    await session.commit()


async def update_user(user_id: int, user_in: UserUpdate, session: AsyncSession):
    update_data = user_in.dict(exclude_unset=True)
    stmt = (
        update(User).
        where(User.id == user_id).
        values(**update_data)
    )
    await session.execute(stmt)
    await session.commit()
