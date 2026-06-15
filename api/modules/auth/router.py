from fastapi import APIRouter, Security

from core.deps import permission_check
from shared.base_schema import SuccessResponse
from modules.system.models import User
from modules.auth.schemas import LoginSchema
from modules.auth.service import auth_service

router = APIRouter(prefix="/auth", tags=["认证管理"])


@router.post("/login")
async def login(payload: LoginSchema):
    token, refresh_token = await auth_service.login(
        username=payload.username, password=payload.password,
    )
    return SuccessResponse(data={"token": token, "refreshToken": refresh_token})


@router.post("/logout")
async def logout(current_user: User = Security(permission_check)):
    await auth_service.logout(current_user.id)
    return SuccessResponse(data={"msg": "退出登录成功"})
