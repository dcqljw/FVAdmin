import random
import string

from fastapi import APIRouter, Depends, Security

from core.security import get_password_hash, verify_password
from models.menu_model import Menu
from models.user_model import User, UserPydantic, UserPydanticList
from models.role_model import Role, RolePydantic, RolePydanticList
from router.deps import verify_token_dep, get_current_user, permission_check
from schemas.response import SuccessResponse, ErrorResponse
from schemas.user import UserCreateSchema, EditPasswordSchema
from schemas.role import RoleCreateSchema, RoleMenuCreateSchema

router = APIRouter(prefix="/user", tags=["用户管理"])


@router.get("/info")
async def get_user_info(user: User = Depends(get_current_user)):
    user = await UserPydantic.from_tortoise_orm(user)
    user = user.model_dump(mode="json", exclude={"password"})
    return SuccessResponse(data=user)


@router.get("/list")
async def get_user(user: User = Depends(get_current_user),
                   current: int = 1,
                   size: int = 10,
                   username: str = None,
                   phone: str = None,
                   email: str = None,
                   ):
    query = User.all()
    if username:
        query = query.filter(username__contains=username)
    if phone:
        query = query.filter(phone__contains=phone)
    if email:
        query = query.filter(email__contains=email)
    user_roles_model = await query.offset((current - 1) * size).limit(
        size).all().prefetch_related("roles")
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
        role = await Role.filter(code__in=user.role)
        create_user = await User.create(**user.model_dump())
        await create_user.roles.add(*role)
        return SuccessResponse(data={"msg": "添加用户成功"})


@router.post('/edit')
async def edit_user(user_in: UserCreateSchema, permission: str = Security(permission_check, scopes=['user:edit'])):
    user = await User.get_or_none(username=user_in.username)
    if user:
        user.nickname = user_in.nickname
        user.phone = user_in.phone
        user.email = user_in.email
        user.avatar = user_in.avatar
        await user.roles.clear()
        await user.save()
        role = await Role.filter(code__in=user_in.role)
        await user.roles.add(*role)
        return SuccessResponse(data={"msg": "修改用户成功"})
    else:
        return ErrorResponse(msg="用户不存在")


@router.post('/delete')
async def delete_user(user_id: int, permission: str = Security(permission_check, scopes=['user:delete'])):
    if user_id == permission.id:
        return ErrorResponse(msg="不能删除自己")
    user = await User.get_or_none(id=user_id)
    if user.username == "admin":
        return ErrorResponse(msg="超级管理员无法删除")
    if user:
        await user.delete()
        return SuccessResponse(data={"msg": "删除用户成功"})
    else:
        return ErrorResponse(msg="用户不存在")


@router.post('/edit-password')
async def edit_password(password_in: EditPasswordSchema, current_user: User = Depends(get_current_user)):
    user_data = await User.get_or_none(username=current_user.username)
    if user_data:
        if verify_password(password_in.old_password, user_data.password):
            password = get_password_hash(password_in.new_password)
            user_data.password = password
            await user_data.save()
            return SuccessResponse(data={"msg": "修改密码成功"})
        else:
            return ErrorResponse(msg="原密码错误")
    else:
        return ErrorResponse(msg="原密码错误")


@router.post('/reset-password')
async def reset_password(user_id: int, permission: str = Security(permission_check, scopes=['user:reset-password'])):
    user = await User.get_or_none(id=user_id)
    if user:
        random_str = string.ascii_lowercase + string.ascii_uppercase + string.digits
        new_password = "".join(random.choices(random_str, k=8))
        user.password = get_password_hash(new_password)
        await user.save()
        return SuccessResponse(data={"new_password": new_password})
    else:
        return ErrorResponse(msg="用户不存在")
