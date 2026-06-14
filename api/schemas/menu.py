from enum import Enum
from typing import Any

from pydantic import BaseModel


class MenuType(Enum):
    MENU = 1
    BUTTON = 2
    DIRECTORY = 3


class MenuBaseSchema(BaseModel):
    name: str
    path: str
    meta: dict[str, Any]
    component: str
    sort: int
    status: bool
    auth_mark: str
    type: int


class MenuCreateSchema(MenuBaseSchema):
    parent_id: int


class MenuEditSchema(MenuBaseSchema):
    id: int


class AddRoleMenuSchema(BaseModel):
    role_id: int
    menu_ids: list[int]
