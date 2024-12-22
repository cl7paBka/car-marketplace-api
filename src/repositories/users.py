from src.utils.repository import SQLAlchemyRepository
from src.models.models import Users


class UsersRepository(SQLAlchemyRepository):
    model = Users
