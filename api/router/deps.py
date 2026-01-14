from typing import Annotated, Optional

from fastapi import Depends, Header, Request, Security
from fastapi.security import APIKeyHeader, SecurityScopes
from fastapi.exceptions import HTTPException

from core.security import verify_token
from custom_exception import CustomException
from models.user_model import User

API_KEY_HEADER = APIKeyHeader(
    name="Authorization",
    scheme_name="API key",
    description="Enter your API key",
    auto_error=False,
)


async def verify_token_dep(token: Optional[str] = Depends(API_KEY_HEADER)):
    payload = verify_token(token)
    if payload:
        return payload.get("uid", '')
    raise HTTPException(status_code=401, detail="登录过期,请重新登录!")


async def get_current_user(uid: str = Depends(verify_token_dep)):
    user = await User.get_or_none(id=uid)
    if user:
        return user
    else:
        raise HTTPException(status_code=401, detail="登录过期,请重新登录!")


async def permission_check(security_scopes: SecurityScopes, user: User = Depends(get_current_user)) -> User:
    menus = await user.roles.all().prefetch_related("menus")
    for i in menus:
        for j in i.menus:
            if j.auth_mark in security_scopes.scopes:
                return user
    raise CustomException(code=4001, msg="权限不足")
