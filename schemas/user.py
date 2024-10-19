from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    """
    Schema for creating a new user.

    All fields are required to ensure the creation of a valid user object.
    """
    name: str
    surname: str
    nickname: str
    email: EmailStr


class UserInfo(BaseModel):
    """
    Schema for updating or displaying user information.

    All fields are optional for flexible updates or display.
    """
    name: Optional[str] = None
    surname: Optional[str] = None
    nickname: Optional[str] = None
    email: Optional[EmailStr] = None


class UserInDB(UserInfo):
    """
    Schema representing a user stored in the database.

    Includes a unique identifier for each user.
    """
    id: int
