from polyfactory.factories.pydantic_factory import ModelFactory

from auth.models import User


class UserFactory(ModelFactory[User]):
    __model__ = User
