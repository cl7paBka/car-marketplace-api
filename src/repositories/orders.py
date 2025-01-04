from src.utils.repository import SQLAlchemyRepository
from src.models.models import Orders


class OrdersRepository(SQLAlchemyRepository):
    model = Orders
