from datetime import timedelta

from shared.log_config import api_logger
from shared.redis_client import redis_cache
from shared.captcha_service import captcha_service
from core.config import settings
from core.security import create_access_token
from core.exceptions import CustomException
# 跨模块通信：仅通过 system 的 PublicService，不直接访问其 repository / models
from modules.system.service import system_public_service


class AuthService:
    """认证服务：登录签发 token、登出失效 token"""

    TOKEN_TTL_DAYS = 7

    async def login(
        self,
        username: str,
        password: str,
        captcha_key: str | None = None,
        captcha_code: str | None = None,
    ) -> tuple[str, str]:
        api_logger.info(f"用户 {username} 尝试登录")

        # ---- 验证码校验 ----
        if settings.CAPTCHA_ENABLED:
            if not captcha_key or not captcha_code:
                raise CustomException(code=400, msg="请提供验证码")
            await captcha_service.validate(captcha_key, captcha_code)

        # ---- 凭证校验 ----
        user = await system_public_service.verify_credentials(username, password)
        if not user:
            api_logger.warning(f"用户 {username} 登录失败：账户或密码错误")
            raise CustomException(code=401, msg="账户或密码错误")

        token = create_access_token(
            data={"uid": user.id, "username": user.username},
            expire_minutes=timedelta(days=self.TOKEN_TTL_DAYS),
        )

        # 单点登录：将新 token 存入 Redis，旧 token 失效
        await redis_cache.set(
            f"user_token:{user.id}", token, ttl=self.TOKEN_TTL_DAYS * 24 * 3600
        )

        api_logger.info(f"用户 {username} 登录成功")
        return token, token

    @staticmethod
    async def logout(user_id: int) -> None:
        await redis_cache.delete(f"user_token:{user_id}")


auth_service = AuthService()
