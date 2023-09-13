from pydantic_factories import ModelFactory

from auth.models import User


class UserFactory(ModelFactory):
    __model__ = User

# Что-то не идёт...