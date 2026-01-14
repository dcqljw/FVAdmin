from fastapi import APIRouter, Depends, Security
from tortoise.expressions import Q

from models.user_model import User
from models.role_model import Role, RolePydanticList
from router.deps import permission_check
from schemas.response import SuccessResponse, ErrorResponse
from schemas.role import RoleCreateSchema
from core.log_config import api_logger

router = APIRouter(prefix="/role", tags=["角色管理"])


@router.get("/list")
async def get_role_list(current: int = 1,
                        size: int = 10,
                        name: str = None,
                        code: str = None,
                        description: str = None
                        ):
    api_logger.info(f"查询角色列表，参数：page={current}, size={size}, name={name}, code={code}, description={description}")
    query = Role.all()
    if name:
        query = query.filter(name__contains=name)
    if code:
        query = query.filter(code__contains=code)
    if description:
        query = query.filter(description__contains=description)
    roles = await query.offset((current - 1) * size).limit(size).all()
    api_logger.info(f"查询角色列表成功，返回 {len(roles)} 条记录")
    return SuccessResponse(data=RolePydanticList(roles))


@router.post("/add")
async def add_role(role: RoleCreateSchema, current_user: User = Security(permission_check, scopes=['role:add'])):
    api_logger.info(f"用户 {current_user.username} 尝试添加角色 {role.name} (代码: {role.code})")
    is_role = await Role.filter(Q(name=role.name) | Q(code=role.code)).first()
    if is_role:
        api_logger.warning(f"添加角色失败：角色 {role.name} 或代码 {role.code} 已存在")
        return ErrorResponse(msg="角色已存在")
    else:
        await Role.create(**role.model_dump())
        api_logger.info(f"用户 {current_user.username} 成功添加角色 {role.name}")
        return SuccessResponse(data={"msg": "添加角色成功"})


@router.post('/delete')
async def delete_role(role_id: int, current_user: User = Security(permission_check, scopes=['role:delete'])):
    api_logger.info(f"用户 {current_user.username} 尝试删除角色ID {role_id}")
    if role_id == current_user.id:
        api_logger.warning(f"用户 {current_user.username} 尝试删除自己，操作被拒绝")
        return ErrorResponse(msg="不能删除自己")
    role = await Role.get_or_none(id=role_id)
    if role:
        if role.code == 'R_ADMIN':
            api_logger.warning(f"用户 {current_user.username} 尝试删除超级管理员角色，操作被拒绝")
            return ErrorResponse(msg="超级管理员无法删除")
        await role.delete()
        api_logger.info(f"用户 {current_user.username} 成功删除角色 {role.name}")
        return SuccessResponse(data={"msg": "删除角色成功"})
    else:
        api_logger.warning(f"删除角色失败：角色ID {role_id} 不存在")
        return ErrorResponse(msg="角色不存在")


@router.post('/edit')
async def edit_role(role_in: RoleCreateSchema, current_user: User = Security(permission_check, scopes=['role:edit'])):
    api_logger.info(f"用户 {current_user.username} 尝试编辑角色 {role_in.code}")
    role = await Role.get_or_none(code=role_in.code)
    if role:
        role.name = role_in.name
        role.description = role_in.description
        role.enabled = role_in.enabled
        await role.save()
        api_logger.info(f"用户 {current_user.username} 成功编辑角色 {role_in.code}")
        return SuccessResponse(data={"msg": "修改角色成功"})
    else:
        api_logger.warning(f"编辑角色失败：角色代码 {role_in.code} 不存在")
        return ErrorResponse(msg="角色不存在")
