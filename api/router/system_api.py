from fastapi import APIRouter

from schemas.role import RoleCreateSchema
from models.role_model import Role

router = APIRouter(prefix="/system", tags=["系统管理"])


@router.post("/add_role")
async def add_role(role: RoleCreateSchema):
    role = Role.create(**role.model_dump())
    return role


@router.post("/add_menu")
async def add_menu(menu: dict):
    return {"message": "添加菜单成功"}


@router.post("/add_permission")
async def add_permission(permission: dict):
    return {"message": "添加权限成功"}
