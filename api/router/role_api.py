from fastapi import APIRouter, Depends

from models.user_model import User
from models.role_model import Role, RolePydanticList
from router.deps import get_current_user
from schemas.response import SuccessResponse, ErrorResponse

router = APIRouter(prefix="/role", tags=["角色管理"])


@router.get("/list")
async def get_role_list():
    return SuccessResponse(data=RolePydanticList(await Role.filter().all()))


@router.post("/")
async def get_role(user: User = Depends(get_current_user)):
    roles_all = await user.roles.all()
    roles = [i.code for i in roles_all]
    if "R_ADMIN" in roles:
        role_all = await Role.filter().all()
        role_list = RolePydanticList(role_all)
        return SuccessResponse(data=role_list)
    else:
        return ErrorResponse(msg="无权限")
