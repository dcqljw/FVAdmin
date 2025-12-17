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
    meta: dict[str, Any]
    component: str
    sort: int
    status: bool
    auth_mark: str
    type: int


class AddRoleMenuSchema(BaseModel):
    role_id: int
    menu_ids: list[int]
