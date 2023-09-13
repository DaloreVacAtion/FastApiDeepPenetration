from polyfactory.factories import DataclassFactory

from auth.models import User


# @dataclass
# class User:
#     id: int
#     username: str
#     name: str
#     age: int
#     email: Mapped[str]
#     hashed_password: Mapped[str]
#     is_active: Mapped[bool]
#     is_superuser: Mapped[bool]
#     is_verified: Mapped[bool]


class UserFactory(DataclassFactory[User]):
    __model__ = User

