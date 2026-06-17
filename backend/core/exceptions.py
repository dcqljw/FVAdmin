from typing import Optional, Any

from fastapi.responses import JSONResponse
from fastapi.requests import Request


class CustomException(Exception):
    def __init__(
            self,
            code: int = 400,
            msg: str = "业务异常",
            data: Optional[Any] = None
    ):
        self.code = code
        self.msg = msg
        self.data = data
        super().__init__(self.msg)


# 1. 处理自定义业务异常
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=200,  # HTTP 状态码固定200（业务码用code字段区分）
        content={
            "code": exc.code,
            "msg": exc.msg,
            "data": exc.data
        }
    )
