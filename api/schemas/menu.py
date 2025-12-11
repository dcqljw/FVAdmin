from enum import Enum
from typing import Any

from pydantic import BaseModel


class MenuType(Enum):
    MENU = 1
    BUTTON = 2
    DIRECTORY = 3


class MenuCreateSchema(BaseModel):
    parent_id: int
    name: str
    path: str
    menu_type: int
    meta: dict[str, Any]
    component: str


class AddRoleMenuSchema(BaseModel):
    role_id: int
    menu_ids: list[int]
