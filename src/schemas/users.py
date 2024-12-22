from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from src.utils.enums import Role


class UserCreate(BaseModel):
    name: str
    surname: str
    email: EmailStr
    role: Role


class UserUpdate(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[Role] = None


class UserSchema(BaseModel):
    id: int
    name: str
    surname: str
    email: EmailStr
    role: Role
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True