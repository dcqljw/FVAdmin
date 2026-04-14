from fastapi import APIRouter

from schemas.user import UserLoginSchema
from schemas.response import SuccessResponse
from services import auth_service

router = APIRouter(prefix="/auth", tags=['auth'])


@router.post("/login")
async def login(user: UserLoginSchema):
    token, refresh_token = await auth_service.authenticate(
        username=user.username, password=user.password,
    )
    return SuccessResponse(data={"token": token, "refreshToken": refresh_token})
