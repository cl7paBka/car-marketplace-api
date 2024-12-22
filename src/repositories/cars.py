from src.utils.repository import SQLAlchemyRepository
from src.models.models import Cars


class CarsRepository(SQLAlchemyRepository):
    model = Cars
