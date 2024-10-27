from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional
from src.db.models import Role


class UserCreate(BaseModel):
    """
    Schema for creating a new user.

    All fields are required to ensure the creation of a valid user object.
    """
    name: str
    surname: str
    email: EmailStr
    role: Role


class UserInfo(BaseModel):
    """
    Schema for updating or displaying user information.

    All fields are optional for flexible updates or display.
    """
    name: Optional[str] = None
    surname: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[Role] = None


class UserInDB(BaseModel):
    """
    Schema representing a user stored in the database.

    Includes a unique identifier, role, and timestamps (created_at, updated_at).
    """
    id: int
    name: str
    surname: str
    email: EmailStr
    role: str
    created_at: datetime  # Include created_at timestamp
    updated_at: Optional[datetime] = None  # Include updated_at timestamp (can be None if not updated yet)

    class Config:
        from_attributes = True
