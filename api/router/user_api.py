from fastapi import APIRouter, Depends

from models.user_model import User, UserPydantic
from router.deps import verify_token_dep
from schemas.response import SuccessResponse, ErrorResponse

router = APIRouter(prefix="/user", tags=["用户管理"])


@router.post("/user_info")
async def user_info(uid: str = Depends(verify_token_dep)):
    user = await User.get_or_none(id=uid)
    if user:
        user = await UserPydantic.from_tortoise_orm(user)
        user = user.model_dump(exclude={"password"})
        return SuccessResponse(data=user)
    else:
        return ErrorResponse(message="用户不存在")
