from fastapi import APIRouter, Depends

from models.user_model import User
from router.deps import get_current_user
from schemas.user import UserLoginSchema
from schemas.response import SuccessResponse
from services import auth_service
from core.redis_client import redis_cache

router = APIRouter(prefix="/auth", tags=['auth'])


@router.post("/login")
async def login(user: UserLoginSchema):
    token, refresh_token = await auth_service.authenticate(
        username=user.username, password=user.password,
    )
    return SuccessResponse(data={"token": token, "refreshToken": refresh_token})


@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    await redis_cache.delete(f"user_token:{current_user.id}")
    return SuccessResponse(data={"msg": "退出登录成功"})
