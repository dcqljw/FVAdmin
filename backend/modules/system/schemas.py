from typing import Any

from pydantic import BaseModel


# ========== User Schemas ==========

class UserCreateSchema(BaseModel):
    username: str
    password: str
    nickname: str
    email: str | None = None
    phone: str | None = None
    avatar: str | None = None
    role: list[str]


class EditPasswordSchema(BaseModel):
    old_password: str
    new_password: str


# ========== Role Schemas ==========

class RoleCreateSchema(BaseModel):
    name: str
    code: str
    description: str
    enabled: bool


# ========== Menu Schemas ==========

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
