from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Column, Integer, String, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    """
    Модель пользователя для ДБ
    """
    # поля нашего пользвоателя
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    name = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    # поля библиотеки fastapi_users
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )