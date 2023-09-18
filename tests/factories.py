import factory
import faker

from auth.models import User


class SQLAlchemyFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session_persistence = 'flush'

    @classmethod
    def save_db_session(cls, session) -> None:
        cls._meta.sqlalchemy_session = session

        for cls_attr in vars(cls).values():
            if hasattr(cls_attr, 'get_factory'):
                cls_attr.get_factory().save_db_session(session=session)


class UserModelFactory(SQLAlchemyFactory):
    class Meta:
        model = User
