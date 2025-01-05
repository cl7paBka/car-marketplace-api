from typing import Annotated, List

from fastapi import APIRouter, Depends
from pydantic import EmailStr

from src.api.dependencies import users_service
from src.api.responses.users_responses import (
    create_user_responses,
    get_user_by_id_responses,
    get_user_by_email_responses,
    get_users_by_role_responses,
    get_all_users_responses,
    update_user_responses,
    delete_user_responses,
)
from src.schemas.users import (
    UserCreateSchema,
    UserUpdateSchema,
    UserSchema
)
from src.schemas.base_response import (
    BaseResponse,
    BaseStatusMessageResponse
)
from src.services.users import UsersService
from src.utils.enums import Role

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# TODO: Make better end-points

@router.post(  # TODO: Add information about user roles in description in create end-point
    path="/create",
    response_model=BaseResponse[UserSchema],
    summary="Create a new user",
    description="""
    Create a new user with the provided data.

    - Before creating, the system checks if a user with the same email already exists.
    - If a user with the same email is found, the process will stop, and a 409 Conflict status code will be returned.
    """,
    responses=create_user_responses
)
async def create_user(
        user: UserCreateSchema,
        service: Annotated[UsersService, Depends(users_service)]
):
    return await service.create(user)


@router.get(
    path="/{user_id}",
    response_model=BaseResponse[UserSchema],
    summary="Get user by ID",
    description="""
    Retrieve detailed information about a specific user by their unique ID.

    - If no user is found with the given ID, a 404 Not Found status code will be returned.
    """,
    responses=get_user_by_id_responses
)
async def get_user_by_id(
        user_id: int,
        service: Annotated[UsersService, Depends(users_service)]
):
    filter_by = {"id": user_id}
    return await service.get_one_by_filter(**filter_by)


@router.get(
    path="/email/{user_email}",
    response_model=BaseResponse[UserSchema],
    summary="Get user by email",
    description="""
    Retrieve a user by their email address.

    - Checks if the provided email is valid.
    - If no user is found with the given email, a 404 Not Found status code will be returned.
    """,
    responses=get_user_by_email_responses
)
async def get_user_by_email(
        user_email: EmailStr,
        service: Annotated[UsersService, Depends(users_service)]
):
    filter_by = {"email": user_email}
    return await service.get_one_by_filter(**filter_by)


@router.get(
    path="/role/{role}",
    response_model=BaseResponse[List[UserSchema]],
    summary="Get users by role",
    description="""
    Retrieve a list of users filtered by their role.

    - Returns users with the specified role.
    - If no users are found, an empty list will be returned with a 200 OK status code.
    """,
    responses=get_users_by_role_responses
)
async def get_users_by_role(
        role: Role,
        service: Annotated[UsersService, Depends(users_service)]
):
    filter_by = {"role": role}
    return await service.get_many_by_filter(**filter_by)


@router.get(
    path="/",
    response_model=BaseResponse[List[UserSchema]],
    summary="Get all users",
    description="""
    Retrieve a complete list of all users in the system.

    - Returns all registered users.
    - If no users are found, an empty list will be returned with a 200 OK status code.
    """,
    responses=get_all_users_responses
)
async def get_all_users(
        service: Annotated[UsersService, Depends(users_service)]
):
    return await service.get_all()


@router.patch(
    path="/patch/{user_id}",
    response_model=BaseResponse[UserSchema],
    summary="Update user details",
    description="""
    Update the details of a specific user by their unique ID.

    - First, checks if a user with the given ID exists. If not, a 404 Not Found status code will be returned.
    - If the email field is being updated, the system checks if another user already has the same email.
      If a duplicate is found, a 409 Conflict status code will be returned.
    - You can update only the fields you need, leaving others unchanged.
    """,
    responses=update_user_responses
)
async def update_user_by_user_id(
        user_id: int,
        new_user: UserUpdateSchema,
        service: Annotated[UsersService, Depends(users_service)]
):
    return await service.update_by_id(user_id, new_user)


@router.delete(
    path="/delete/{user_id}",
    response_model=BaseStatusMessageResponse,
    summary="Delete a user",
    description="""
    Delete a specific user by their unique ID.

    - Checks if the user exists before deleting. If no user is found, a 404 Not Found status code will be returned.
    - Permanently removes the user from the system if they exist.
    """,
    responses=delete_user_responses
)
async def delete_user_by_user_id(
        user_id: int,
        service: Annotated[UsersService, Depends(users_service)]
):
    return await service.delete_by_id(user_id)
