from datetime import timedelta

from fastapi import APIRouter

from core.security import verify_password, create_access_token
from models.user_model import User
from schemas.user import UserLoginSchema
from schemas.response import SuccessResponse, ErrorResponse

router = APIRouter(prefix="/auth", tags=['auth'])


@router.post("/login")
async def login(user: UserLoginSchema):
    user_data = await User.get_or_none(username=user.username)
    print(user_data)
    if user_data:
        if verify_password(user.password, user_data.password):
            token = create_access_token(data={"uid": user_data.id}, expire_minutes=timedelta(days=7))
            return SuccessResponse(data=token)
        else:
            return ErrorResponse(message="账户或密码错误")
    else:
        return ErrorResponse(message="账户或密码错误")
