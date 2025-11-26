from fastapi import APIRouter, Depends

from core.security import get_password_hash
from models.user_model import User, UserPydantic
from router.deps import verify_token_dep
from schemas.response import SuccessResponse, ErrorResponse
from schemas.user import UserCreateSchema

router = APIRouter(prefix="/user", tags=["用户管理"])


@router.post("/add_user")
async def add_user(user: UserCreateSchema):
    is_in_user = await User.get_or_none(username=user.username)
    if is_in_user:
        return ErrorResponse(message="用户已存在")
    else:
        user.password = get_password_hash(user.password)
        user = await User.create(**user.model_dump())
        if user:
            return SuccessResponse(data={"id": user.id})
        else:
            return ErrorResponse(message="添加用户失败")


@router.post("/user_info")
async def user_info(uid: str = Depends(verify_token_dep)):
    user = await User.get_or_none(id=uid)
    if user:
        user = await UserPydantic.from_tortoise_orm(user)
        user = user.model_dump(exclude={"password"})
        return SuccessResponse(data=user)
    else:
        return ErrorResponse(message="用户不存在")
