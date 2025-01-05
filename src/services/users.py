from typing import Any, Dict, List

from sqlalchemy.exc import NoResultFound

from src.schemas.base_response import (
    BaseResponse,
    BaseStatusMessageResponse
)
from src.schemas.users import (
    UserCreateSchema,
    UserSchema,
    UserUpdateSchema
)
from src.utils.exception_handler import (
    handle_exception,
    handle_exception_default_500
)
from src.utils.repository import AbstractRepository


# TODO: Simplify by reducing nesting
#  Make helper methods like `check_user_exists_by_id` and `check_email_uniqueness` or other
class UsersService:
    """
    Service layer for managing users.

    This class provides methods to handle user-related operations, such as
    creating, retrieving, updating, and deleting users. It acts as a bridge
    between the repository layer and the application layer.
    """

    def __init__(self, users_repo: AbstractRepository):
        """
        Initialize the UsersService with a user repository.
        """
        self.users_repo = users_repo

    async def create(self, user: UserCreateSchema) -> BaseResponse[UserSchema]:
        """
        Create a new user after verifying that the email is unique.
        """
        # Check if user exists by unique email
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
            return BaseResponse[UserSchema](
                status="success",
                message="User created.",
                data=created_user
            )

        except Exception as e:
            handle_exception_default_500(e)

    async def get_one_by_filter(self, **filter_by: Dict[str, Any]) -> BaseResponse[UserSchema]:
        """
        Retrieve a single user based on the given filter criteria.
        """
        try:
            user = await self.users_repo.get_one(**filter_by)
            if user:  # Is not None
                return BaseResponse[UserSchema](
                    status="success",
                    message="User found.",
                    data=user
                )

        except Exception as e:
            # Catch unexpected error
            handle_exception_default_500(e)
        # If user not found
        handle_exception(status_code=404, custom_message="User not found.")

    async def get_many_by_filter(self, **filter_by: Dict[str, Any]) -> BaseResponse[List[UserSchema]]:
        """
        Retrieve all users by specified criteria.
        """
        try:
            users_by_criteria = await self.users_repo.get_many(**filter_by)
            if users_by_criteria:
                return BaseResponse[List[UserSchema]](
                    status="success",
                    message=f"Users found.",
                    data=users_by_criteria
                )
            return BaseResponse[List[UserSchema]](
                # If there are no users by this criteria in db, returns empty users_by_role
                status="error",
                message=f"No users found.",
                data=users_by_criteria
            )
        except Exception as e:
            # Catch unexpected error
            handle_exception_default_500(e)

    async def get_all(self) -> BaseResponse[List[UserSchema]]:
        """
        Retrieve all users in the system.
        """
        try:
            all_users = await self.users_repo.get_all()
            if all_users:  # If there are users return them
                return BaseResponse[List[UserSchema]](
                    status="success",
                    message=f"All users found.",
                    data=all_users
                )

            return BaseResponse[List[UserSchema]](  # If there are no users return empty all_users
                status="error",
                message=f"No users found.",
                data=all_users
            )

        except Exception as e:
            # Catch unexpected error
            handle_exception_default_500(e)

    async def update_by_id(self, user_id: int, user: UserUpdateSchema) -> BaseResponse[UserSchema]:
        """
        Update the details of a user by their ID, ensuring email uniqueness if updated.
        """
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
            return BaseResponse[UserSchema](
                status="success",
                message="User updated.",
                data=updated_user
            )

        except Exception as e:
            handle_exception_default_500(e)

    async def delete_by_id(self, user_id: int) -> BaseStatusMessageResponse:
        """
        Delete a user by their ID.
        """
        try:
            await self.users_repo.delete_one(user_id)
            return BaseStatusMessageResponse(
                status="success",
                message=f"User with id {user_id} deleted."
            )
        except NoResultFound:  # Catches if there is no user with this id
            handle_exception(
                status_code=404,
                custom_message=f"No user with id: '{user_id}' found."
            )
        except Exception as e:
            handle_exception_default_500(e)
