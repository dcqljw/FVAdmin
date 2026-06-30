import base64
import random
import string

from captcha.image import ImageCaptcha

from shared.log_config import api_logger
from shared.redis_client import redis_cache
from core.exceptions import CustomException


class CaptchaService:
    """字符验证码生成与校验服务"""

    # 排除易混淆字符：0/O, 1/I/L
    CHARSET = [c for c in string.ascii_uppercase + string.digits if c not in {"0", "O", "1", "I", "L"}]

    def __init__(self, width: int = 160, height: int = 60, font_sizes: tuple[int, ...] = (38,)):
        self._image = ImageCaptcha(width=width, height=height, font_sizes=font_sizes)

    def generate(self) -> tuple[str, str]:
        """生成 4 位验证码，返回 (验证码文本, base64 data URI)"""
        text = "".join(random.choices(self.CHARSET, k=4))
        buf = self._image.generate(text)
        b64 = base64.b64encode(buf.getvalue()).decode()
        api_logger.debug(f"生成验证码: {text}")
        return text, f"data:image/png;base64,{b64}"

    async def validate(self, captcha_key: str, captcha_code: str) -> None:
        """校验验证码，成功后自动销毁（防重放）；失败则抛出 CustomException"""
        stored = await redis_cache.get(f"captcha:{captcha_key}")
        if not stored:
            raise CustomException(code=400, msg="验证码已过期，请刷新")

        if stored.lower() != captcha_code.lower():
            raise CustomException(code=400, msg="验证码错误")

        # 验证成功后删除，防止重放
        await redis_cache.delete(f"captcha:{captcha_key}")


captcha_service = CaptchaService()
