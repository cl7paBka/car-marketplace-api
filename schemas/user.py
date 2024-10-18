from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    name: str
    surname: str
    nickname: str
    email: EmailStr


class UserInfo(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    nickname: Optional[str] = None
    email: Optional[EmailStr] = None


class UserInDB(UserInfo):
    id: int
