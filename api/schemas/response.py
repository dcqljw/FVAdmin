from typing import Optional, TypeVar, Generic
from pydantic import BaseModel

T = TypeVar("T")


class SuccessResponse(BaseModel, Generic[T]):
    code: int = 200
    message: str = "操作成功"
    data: Optional[T] = None


class ErrorResponse(BaseModel, Generic[T]):
    code: int = 500
    msg: str = "操作失败"
    data: Optional[T] = None
