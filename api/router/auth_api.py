from datetime import timedelta

from fastapi import APIRouter

from tortoise.contrib.pydantic import pydantic_model_creator

from core.security import get_password_hash, verify_password, create_access_token
from models.user_model import User, UserPydantic
from models.role_model import Role
from schemas.user import UserCreateSchema, UserLoginSchema
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


@router.post("/add_user")
async def add_user(user: UserCreateSchema):
    print(user.model_dump())
    user.password = get_password_hash(user.password)
    user = await User.create(**user.model_dump())
    return user
