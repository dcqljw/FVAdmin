from fastapi import APIRouter, Depends

from core.security import get_password_hash
from models.menu_model import Menu
from models.user_model import User, UserPydantic
from models.role_model import Role
from router.deps import verify_token_dep
from schemas.response import SuccessResponse, ErrorResponse
from schemas.user import UserCreateSchema
from schemas.role import RoleCreateSchema, RoleMenuCreateSchema

router = APIRouter(prefix="/user", tags=["用户管理"])


@router.post("/add_user")
async def add_user(user: UserCreateSchema):
    is_in_user = await User.get_or_none(username=user.username)
    if is_in_user:
        return ErrorResponse(message="用户已存在")
    else:
        user.password = get_password_hash(user.password)
        user = await User.create(**user.model_dump())
        if user:
            return SuccessResponse(data={"id": user.id})
        else:
            return ErrorResponse(message="添加用户失败")


@router.post("/user_info")
async def user_info(uid: str = Depends(verify_token_dep)):
    user = await User.get_or_none(id=uid)
    if user:
        user = await UserPydantic.from_tortoise_orm(user)
        user = user.model_dump(exclude={"password"})
        return SuccessResponse(data=user)
    else:
        return ErrorResponse(message="用户不存在")


@router.post("/add_role")
async def add_role(role: RoleCreateSchema):
    role = await Role.create(**role.model_dump())
    return SuccessResponse(data={"id": role.id})


@router.post("/add_user_role")
async def add_user_role(role_id: int, uid: str = Depends(verify_token_dep)):
    user = await User.get_or_none(id=uid)
    if user:
        role = await Role.get_or_none(id=role_id)
        if role:
            await user.roles.add(role)
            return SuccessResponse(data={"message": "添加角色成功"})
        else:
            return ErrorResponse(message="角色不存在")
    else:
        return ErrorResponse(message="用户不存在")


@router.post("/add_menu_permission")
async def add_menu_permission(role_menu: RoleMenuCreateSchema):
    role_id = role_menu.role_id
    menu_id_list = role_menu.menu_id
    role = await Role.get(id=role_id)
    await role.menus.clear()
    for i in menu_id_list:
        menu = await Menu.get(id=i)
        await role.menus.add(menu)
    return {"message": "添加权限成功"}
