from fastapi import APIRouter, Depends, Security

from core.security import get_password_hash
from models.menu_model import Menu
from models.user_model import User, UserPydantic, UserPydanticList
from models.role_model import Role, RolePydantic, RolePydanticList
from router.deps import verify_token_dep, get_current_user, permission_check
from schemas.response import SuccessResponse, ErrorResponse
from schemas.user import UserCreateSchema
from schemas.role import RoleCreateSchema, RoleMenuCreateSchema

router = APIRouter(prefix="/user", tags=["用户管理"])


@router.get("/info")
async def get_user(user: User = Depends(get_current_user)):
    user = await UserPydantic.from_tortoise_orm(user)
    user = user.model_dump(mode="json", exclude={"password"})
    return SuccessResponse(data=user)


@router.get("/list")
async def get_user(user: User = Depends(get_current_user), skip: int = 0, limit: int = 10):
    user_roles_model = await User.filter().offset(skip).limit(limit).all().prefetch_related("roles")
    user_list = UserPydanticList(root=user_roles_model).model_dump(mode='json')['root']
    for idx, user in enumerate(user_roles_model):
        user_list[idx]['roles'] = [i.code for i in user.roles]
    return SuccessResponse(data=user_list)


@router.post("/add")
async def add_user(user: UserCreateSchema, permission: str = Security(permission_check, scopes=['user:add'])):
    is_user = await User.get_or_none(username=user.username)
    if is_user:
        return ErrorResponse(msg="用户已存在")
    else:
        user.password = get_password_hash(user.password)
        await User.create(**user.model_dump())
        return SuccessResponse(data={"msg": "添加用户成功"})


@router.post('/edit')
async def edit_user(user: UserCreateSchema, permission: str = Security(permission_check, scopes=['user:edit'])):
    user_id = user.id
    user = await User.get_or_none(id=user_id)
    if user:
        user.username = user.username
        user.nickname = user.nickname
        user.phone = user.phone
        user.email = user.email
        user.avatar = user.avatar
        user.status = user.status
        user.password = get_password_hash(user.password)
        await user.save()
        return SuccessResponse(data={"msg": "修改用户成功"})
    else:
        return ErrorResponse(msg="用户不存在")


@router.post("/users/{user_id}")
async def user_info(user_id: int, uid: str = Depends(verify_token_dep)):
    user = await User.get_or_none(id=uid)
    if user:
        user = await UserPydantic.from_tortoise_orm(user)
        user = user.model_dump(exclude={"password"})
        return SuccessResponse(data=user)
    else:
        return ErrorResponse(msg="用户不存在")


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
            return SuccessResponse(data={"msg": "添加角色成功"})
        else:
            return ErrorResponse(msg="角色不存在")
    else:
        return ErrorResponse(msg="用户不存在")


@router.post("/add_menu_permission")
async def add_menu_permission(role_menu: RoleMenuCreateSchema):
    role_id = role_menu.role_id
    menu_id_list = role_menu.menu_id
    role = await Role.get(id=role_id)
    await role.menus.clear()
    for i in menu_id_list:
        menu = await Menu.get(id=i)
        await role.menus.add(menu)
    return {"msg": "添加权限成功"}
