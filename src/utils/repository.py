from abc import ABC, abstractmethod

from sqlalchemy import insert, select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):
    """Abstract base class defining the contract for repositories."""

    @abstractmethod
    async def create_one(self, data: dict) -> int:
        """Creates a new record and returns its ID."""
        raise NotImplementedError

    @abstractmethod
    async def get_one(self, **filter_by):
        """Fetches a single record based on provided filter criteria."""
        raise NotImplementedError

    @abstractmethod
    async def edit_one(self, id: int, data: dict) -> int:
        """Edits a record by ID and returns its ID."""
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

    async def create_one(self, data: dict) -> int:
        statement = insert(self.model).values(**data).returning(self.model.id)
        result = await self.session.execute(statement)
        await self.session.commit()
        return result.scalar_one()

    async def get_one(self, **filter_by):
        statement = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(statement)
        instance = result.scalar_one_or_none()
        if not instance:
            return None  # Return None if no record is found
        return instance.to_read_model()

    async def edit_one(self, id: int, data: dict) -> int:
        statement = update(self.model).values(**data).filter_by(id=id).returning(self.model.id)
        result = await self.session.execute(statement)
        await self.session.commit()
        return result.scalar_one()

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
