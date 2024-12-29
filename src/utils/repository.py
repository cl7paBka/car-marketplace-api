from abc import ABC, abstractmethod

from sqlalchemy import insert, select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):
    """Abstract base class defining the contract for repositories."""

    @abstractmethod
    async def create_one(self, data: dict):
        """Creates a new record and returns it."""
        raise NotImplementedError

    @abstractmethod
    async def get_one(self, **filter_by):
        """Fetches a single record based on provided filter criteria."""
        raise NotImplementedError

    @abstractmethod
    async def edit_one(self, id: int, data: dict):
        """Edits a record by ID and returns it."""
        raise NotImplementedError

    @abstractmethod
    async def get_all(self):
        """Fetches all records."""
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, id: int) -> int:
        """Deletes a record by ID and returns its ID."""
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_one(self, data: dict):
        statement = insert(self.model).values(**data).returning(self.model)
        result = await self.session.execute(statement)
        await self.session.commit()

        created_entity = result.scalars().first()
        entity = created_entity.to_read_model()
        return entity

    async def get_one(self, **filter_by):
        # Filter by is used for different get functions in services, for example: get by transmission, get by year in
        # src/services/cars.py
        statement = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(statement)
        instance = result.scalar_one_or_none()
        if not instance:
            return None  # Return None if no record is found
        return instance.to_read_model()

    async def edit_one(self, id: int, data: dict):
        # Filter data to exclude None values, because all attributes in db are not nullable
        filtered_data = {key: value for key, value in data.items() if value is not None}

        statement = update(self.model).values(**filtered_data).filter_by(id=id).returning(self.model)
        result = await self.session.execute(statement)
        await self.session.commit()

        updated_entity = result.scalars().first()
        entity = updated_entity.to_read_model()
        return entity

    async def get_all(self):
        statement = select(self.model)
        result = await self.session.execute(statement)
        result = [instance.to_read_model() for instance in result.scalars().all()]
        return result

    async def delete_one(self, id: int) -> int:
        statement = delete(self.model).where(self.model.id == id).returning(self.model.id)
        result = await self.session.execute(statement)
        await self.session.commit()
        return result.scalar_one()
