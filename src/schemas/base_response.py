from typing import Optional, Generic, TypeVar
from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar("T")  # Represents the type of data in the response


class BaseResponse(GenericModel, Generic[T]):
    status: str
    message: str
    data: Optional[T]  # Can be None


class BaseStatusMessageResponse(BaseModel):
    status: str
    message: str
