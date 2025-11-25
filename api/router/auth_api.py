from fastapi import APIRouter

from core.security import get_password_hash
from models.user_model import User
from models.role_model import Role
from schemas.user import UserCreateSchema, UserLoginSchema

router = APIRouter(prefix="/auth", tags=['auth'])


@router.post("/login")
async def login(user: UserLoginSchema):
    return {"message": "login"}


@router.post("/add_user")
async def add_user(user: UserCreateSchema):
    print(user.model_dump())
    user.password = get_password_hash(user.password)
    user = await User.create(**user.model_dump())
    role = await Role.create(name="Admin", description="", status=1)
    await user.roles.add(role)
    return user
