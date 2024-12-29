from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr
from src.utils.enums import Role
from src.schemas.base_response import BaseResponse, BaseStatusMessageResponse


# Input schemas
class UserCreateSchema(BaseModel):
    name: str
    surname: str
    email: EmailStr
    role: Role


class UserUpdateSchema(BaseModel):
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


# Output schemas


class UserCreateResponse(BaseResponse[UserSchema]):
    pass


class UserGetOneResponse(BaseResponse[UserSchema]):
    pass


class UserGetManyResponse(BaseResponse[List[UserSchema]]):
    pass


class UserUpdateResponse(BaseResponse[UserSchema]):
    pass


class UserDeleteResponse(BaseStatusMessageResponse):
    pass
