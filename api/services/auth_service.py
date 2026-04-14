from datetime import timedelta

from core.log_config import auth_logger
from core.security import verify_password, create_access_token
from custom_exception import CustomException
from models.user_model import User


class AuthService:

    async def authenticate(self, username: str, password: str) -> tuple[str, str]:
        user = await User.get_or_none(username=username)
        auth_logger.info(f"用户 {username} 尝试登录")

        if not user:
            auth_logger.warning(f"用户 {username} 不存在")
            raise CustomException(code=401, msg="账户或密码错误")

        if not verify_password(password, user.password):
            auth_logger.warning(f"用户 {username} 密码错误")
            raise CustomException(code=401, msg="账户或密码错误")

        token = create_access_token(
            data={"uid": user.id}, expire_minutes=timedelta(days=7)
        )
        auth_logger.info(f"用户 {username} 登录成功")
        return token, token


auth_service = AuthService()
