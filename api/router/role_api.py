from fastapi import APIRouter, Security

from models.user_model import User
from router.deps import permission_check
from schemas.response import SuccessResponse
from schemas.role import RoleCreateSchema
from services import role_service

router = APIRouter(prefix="/role", tags=["角色管理"])


@router.get("/list")
async def get_role_list(
    current: int = 1,
    size: int = 10,
    name: str = None,
    code: str = None,
    description: str = None,
):
    role_list = await role_service.list_roles(
        current=current, size=size, name=name, code=code, description=description,
    )
    return SuccessResponse(data=role_list)


@router.post("/add")
async def add_role(
    role: RoleCreateSchema,
    current_user: User = Security(permission_check, scopes=['role:add']),
):
    await role_service.create_role(
        name=role.name, code=role.code,
        description=role.description, enabled=role.enabled,
    )
    return SuccessResponse(data={"msg": "添加角色成功"})


@router.post('/delete')
async def delete_role(
    role_id: int,
    current_user: User = Security(permission_check, scopes=['role:delete']),
):
    await role_service.delete_role(role_id=role_id, current_user=current_user)
    return SuccessResponse(data={"msg": "删除角色成功"})


@router.post('/edit')
async def edit_role(
    role_in: RoleCreateSchema,
    current_user: User = Security(permission_check, scopes=['role:edit']),
):
    await role_service.update_role(
        code=role_in.code, name=role_in.name,
        description=role_in.description, enabled=role_in.enabled,
    )
    return SuccessResponse(data={"msg": "修改角色成功"})
