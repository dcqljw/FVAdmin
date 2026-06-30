from typing import Optional

from shared.base_schema import BaseSchema


class LLMModelCreateSchema(BaseSchema):
    name: str
    code: str
    provider: str = ""
    base_url: str
    api_key: str
    model_name: str
    max_tokens: int = 2048
    is_default: bool = False
    status: int = 1


class LLMModelEditSchema(BaseSchema):
    id: int
    name: str
    provider: str = ""
    base_url: str
    api_key: Optional[str] = None  # None=不修改
    model_name: str
    max_tokens: int = 2048
    is_default: bool = False
    status: Optional[int] = None