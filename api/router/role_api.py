from fastapi import APIRouter, Depends, Security
from tortoise.expressions import Q

from models.user_model import User
from models.role_model import Role, RolePydanticList
from router.deps import permission_check
from schemas.response import SuccessResponse, ErrorResponse
from schemas.role import RoleCreateSchema

router = APIRouter(prefix="/role", tags=["角色管理"])


@router.get("/list")
async def get_role_list(current: int = 1,
                        size: int = 10,
                        name: str = None,
                        code: str = None,
                        description: str = None
                        ):
    query = Role.all()
    if name:
        query = query.filter(name__contains=name)
    if code:
        query = query.filter(code__contains=code)
    if description:
        query = query.filter(description__contains=description)
    query = await query.offset((current - 1) * size).limit(size).all()
    return SuccessResponse(data=RolePydanticList(query))


@router.post("/add")
async def add_role(role: RoleCreateSchema, current_user: User = Security(permission_check, scopes=['role:add'])):
    is_role = await Role.filter(Q(name=role.name) | Q(code=role.code)).first()
    if is_role:
        return ErrorResponse(msg="角色已存在")
    else:
        await Role.create(**role.model_dump())
        return SuccessResponse(data={"msg": "添加角色成功"})


@router.post('/delete')
async def delete_role(role_id: int, current_user: User = Security(permission_check, scopes=['role:delete'])):
    if role_id == current_user.id:
        return ErrorResponse(msg="不能删除自己")
    role = await Role.get_or_none(id=role_id)
    if role:
        if role.code == 'R_ADMIN':
            return ErrorResponse(msg="超级管理员无法删除")
        await role.delete()
        return SuccessResponse(data={"msg": "删除角色成功"})
    else:
        return ErrorResponse(msg="角色不存在")


@router.post('/edit')
async def edit_role(role_in: RoleCreateSchema, current_user: User = Security(permission_check, scopes=['role:edit'])):
    role = await Role.get_or_none(code=role_in.code)
    if role:
        role.name = role_in.name
        role.description = role_in.description
        role.enabled = role_in.enabled
        await role.save()
        return SuccessResponse(data={"msg": "修改角色成功"})
    else:
        return ErrorResponse(msg="角色不存在")
