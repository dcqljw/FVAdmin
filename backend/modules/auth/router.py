import uuid

from fastapi import APIRouter, Security

from core.config import settings
from core.deps import permission_check
from core.exceptions import CustomException
from shared.base_schema import SuccessResponse
from shared.captcha_service import captcha_service
from shared.redis_client import redis_cache
from modules.system.models import User
from modules.auth.schemas import LoginSchema
from modules.auth.service import auth_service

router = APIRouter(prefix="/auth", tags=["认证管理"])

CAPTCHA_TTL_SECONDS = 300  # 验证码有效期 5 分钟


@router.get("/captcha")
async def get_captcha():
    """获取字符验证码图片"""
    if not settings.CAPTCHA_ENABLED:
        raise CustomException(code=400, msg="验证码功能未启用")

    captcha_text, image_b64 = captcha_service.generate()
    captcha_key = str(uuid.uuid4())

    await redis_cache.set(f"captcha:{captcha_key}", captcha_text, ttl=CAPTCHA_TTL_SECONDS)

    return SuccessResponse(data={
        "captchaKey": captcha_key,
        "image": image_b64,
    })


@router.post("/login")
async def login(payload: LoginSchema):
    token, refresh_token = await auth_service.login(
        username=payload.username,
        password=payload.password,
        captcha_key=payload.captcha_key,
        captcha_code=payload.captcha_code,
    )
    return SuccessResponse(data={"token": token, "refreshToken": refresh_token})


@router.post("/logout")
async def logout(current_user: User = Security(permission_check)):
    await auth_service.logout(current_user.id)
    return SuccessResponse(data={"msg": "退出登录成功"})
