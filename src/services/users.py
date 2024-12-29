from src.utils.repository import AbstractRepository
from src.schemas.users import (
    UserCreateSchema,
    UserUpdateSchema,
    UserCreateResponse,
    UserGetOneResponse,
    UserGetManyResponse,
    UserUpdateResponse,
    UserDeleteResponse
)
from typing import Dict, Any
from src.utils.enums import Role
from src.utils.exception_handler import (
    handle_exception,
    handle_exception_default_500
)

from sqlalchemy.exc import NoResultFound


# TODO notation and repr
class UsersService:
    def __init__(self, users_repo: AbstractRepository):
        self.users_repo = users_repo

    async def create(self, user: UserCreateSchema) -> UserCreateResponse:
        # Check if user exists
        try:
            existing_user = await self.users_repo.get_one(email=user.email)
        except Exception as e:  # If error while checking for user existence throw HTTPException
            handle_exception_default_500(e)

        if existing_user:  # If user exists raise error
            handle_exception(
                status_code=409,
                custom_message=f"User with email: '{user.email}' already exists.",
            )

        # Creating user if not exists
        try:
            users_dict = user.model_dump()
            created_user = await self.users_repo.create_one(users_dict)
            return UserCreateResponse(
                status="success",
                message="User created.",
                data=created_user
            )

        except Exception as e:
            handle_exception_default_500(e)

    async def get_one_by_filter(self, **filter_by: Dict[str, Any]) -> UserGetOneResponse:
        try:
            user = await self.users_repo.get_one(**filter_by)
            if user:  # Is not None
                return UserGetOneResponse(
                    status="success",
                    message="User found.",
                    data=user
                )

        except Exception as e:
            # Catch unexpected error
            handle_exception_default_500(e)
        # If user not found
        handle_exception(status_code=404, custom_message="User not found.")

    async def get_many_by_role(self, role: Role) -> UserGetManyResponse:
        try:
            all_users = await self.users_repo.get_all()
            users_by_role = [user for user in all_users if user.role == role]
            if users_by_role:  # If there are users with this role in db return users_by_role
                return UserGetManyResponse(
                    status="success",
                    message=f"Users with role: '{role.value}' found",
                    data=users_by_role
                )

            return UserGetManyResponse(  # If there are no users with this role in db returns empty users_by_role
                status="error",
                message=f"Users with role: '{role.value}' not found",
                data=users_by_role
            )
        except Exception as e:
            # Catch unexpected error
            handle_exception_default_500(e)

    async def get_all(self) -> UserGetManyResponse:
        try:
            all_users = await self.users_repo.get_all()
            if all_users:  # If there are users return them
                return UserGetManyResponse(
                    status="success",
                    message=f"All users found",
                    data=all_users
                )

            return UserGetManyResponse(  # If there are no users return empty all_users
                status="error",
                message=f"No users found",
                data=all_users
            )

        except Exception as e:
            # Catch unexpected error
            handle_exception_default_500(e)

    async def update_by_id(self, user_id: int, user: UserUpdateSchema) -> UserUpdateResponse:
        # Check if user with this id exists
        try:
            existing_user_by_id = await self.users_repo.get_one(id=user_id)
        except Exception as e:  # If error while checking for user existence throw HTTPException
            handle_exception_default_500(e)

        if not existing_user_by_id:  # If user does not exist raise error
            handle_exception(
                status_code=404,
                custom_message=f"User with id: '{user_id}' does not exist.",
            )

        # Check if email is not unique and already contains in database
        if user.email:  # if user.email is not NONE
            try:
                existing_user_by_email = await self.users_repo.get_one(email=user.email)
            except Exception as e:  # If error while checking for user existence throw HTTPException
                handle_exception_default_500(e)

            if existing_user_by_email:  # If user with this new email already exists throw HTTPException
                handle_exception(
                    status_code=409,
                    custom_message=f"User with email: '{user.email}' already exists.",
                )

        # If user exists update him
        try:
            users_dict = user.model_dump()
            updated_user = await self.users_repo.edit_one(user_id, users_dict)
            return UserUpdateResponse(
                status="success",
                message="User updated.",
                data=updated_user
            )

        except Exception as e:
            handle_exception_default_500(e)

    async def delete_by_id(self, user_id: int) -> UserDeleteResponse:
        try:
            await self.users_repo.delete_one(user_id)
            return UserDeleteResponse(
                status="success",
                message=f"User with id {user_id} deleted."
            )
        except NoResultFound:  # Catches if there is no
            handle_exception(
                status_code=404,
                custom_message=f"No user with id: '{user_id}' found."
            )
        except Exception as e:
            handle_exception_default_500(e)
