from src.utils.repository import AbstractRepository
from src.schemas.users import UserCreate, UserUpdate


class UsersService:
    def __init__(self, users_repo: AbstractRepository):
        self.users_repo = users_repo

    async def create_user(self, user: UserCreate):
        users_dict = user.model_dump()
        created_user = await self.users_repo.create_one(users_dict)
        return created_user

    async def get_all_users(self):
        all_users = await self.users_repo.get_all()
        return all_users