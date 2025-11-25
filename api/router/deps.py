from fastapi import Depends

from typing import Annotated, Optional

from fastapi import Depends, Header, Request
from fastapi.security import APIKeyHeader
from fastapi.exceptions import HTTPException

from core.security import verify_token

API_KEY_HEADER = APIKeyHeader(
    name="Authorization",
    scheme_name="API key",
    description="Enter your API key",
    auto_error=False,
)


async def verify_token_dep(token: Optional[str] = Depends(API_KEY_HEADER)):
    payload = verify_token(token)
    print(type(payload))
    if payload:
        return payload.get("uid", '')
    raise HTTPException(status_code=401, detail="登录过期,请重新登录!")
