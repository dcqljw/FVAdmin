from typing import Optional, TypeVar, Generic
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

T = TypeVar("T")


class BaseSchema(BaseModel):
    """Pydantic 模型基类：API 字段使用 camelCase"""

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class SuccessResponse(BaseModel, Generic[T]):
    code: int = 200
    message: str = "操作成功"
    data: Optional[T] = None
