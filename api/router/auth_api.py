from datetime import timedelta

from fastapi import APIRouter

from core.security import verify_password, create_access_token
from models.user_model import User
from schemas.user import UserLoginSchema
from schemas.response import SuccessResponse, ErrorResponse
from core.log_config import auth_logger

router = APIRouter(prefix="/auth", tags=['auth'])


@router.post("/login")
async def login(user: UserLoginSchema):
    user_data = await User.get_or_none(username=user.username)
    auth_logger.info(f"用户 {user.username} 尝试登录")
    if user_data:
        if verify_password(user.password, user_data.password):
            token = create_access_token(data={"uid": user_data.id}, expire_minutes=timedelta(days=7))
            auth_logger.info(f"用户 {user.username} 登录成功")
            return SuccessResponse(data={"token": token, "refreshToken": token})
        else:
            auth_logger.warning(f"用户 {user.username} 密码错误")
            return ErrorResponse(msg="账户或密码错误")
    else:
        auth_logger.warning(f"用户 {user.username} 不存在")
        return ErrorResponse(msg="账户或密码错误")
