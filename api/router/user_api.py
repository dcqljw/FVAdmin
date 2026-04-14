from fastapi import APIRouter, Depends, Security, UploadFile

from models.user_model import User
from router.deps import get_current_user, permission_check
from schemas.response import SuccessResponse
from schemas.user import UserCreateSchema, EditPasswordSchema
from services import user_service

router = APIRouter(prefix="/user", tags=["用户管理"])


@router.get("/info")
async def get_user_info(user: User = Depends(get_current_user)):
    user_dict = await user_service.get_user_info(user)
    return SuccessResponse(data=user_dict)


@router.get("/list")
async def get_user_list(
    user: User = Depends(get_current_user),
    current: int = 1,
    size: int = 10,
    username: str = None,
    phone: str = None,
    email: str = None,
):
    user_list, total = await user_service.list_users(
        current=current, size=size,
        username=username, phone=phone, email=email,
    )
    return SuccessResponse(data=user_list)


@router.post("/add")
async def add_user(
    user_in: UserCreateSchema,
    current_user: User = Security(permission_check, scopes=['user:add']),
):
    await user_service.create_user(
        username=user_in.username, password=user_in.password,
        nickname=user_in.nickname, role_codes=user_in.role,
        email=user_in.email, phone=user_in.phone, avatar=user_in.avatar,
    )
    return SuccessResponse(data={"msg": "添加用户成功"})


@router.post('/edit')
async def edit_user(
    user_in: UserCreateSchema,
    current_user: User = Security(permission_check, scopes=['user:edit']),
):
    await user_service.update_user(
        username=user_in.username, nickname=user_in.nickname,
        role_codes=user_in.role, email=user_in.email,
        phone=user_in.phone, avatar=user_in.avatar,
    )
    return SuccessResponse(data={"msg": "修改用户成功"})


@router.post('/edit-profile')
async def edit_profile(
    user_in: UserCreateSchema,
    current_user: User = Depends(get_current_user),
):
    await user_service.update_profile(
        user=current_user, nickname=user_in.nickname,
        email=user_in.email, phone=user_in.phone, avatar=user_in.avatar,
    )
    return SuccessResponse(data={"msg": "修改用户成功"})


@router.post('/upload_avatar')
async def upload_avatar(
    file: UploadFile,
    current_user: User = Depends(get_current_user),
):
    file_content = await file.read()
    avatar_url = await user_service.upload_avatar(
        user=current_user, file_content=file_content,
        filename=file.filename, content_type=file.content_type,
        file_size=file.size,
    )
    return SuccessResponse(data={"msg": "上传成功", "avatar_url": avatar_url})


@router.post('/delete')
async def delete_user(
    user_id: int,
    current_user: User = Security(permission_check, scopes=['user:delete']),
):
    await user_service.delete_user(user_id=user_id, current_user=current_user)
    return SuccessResponse(data={"msg": "删除用户成功"})


@router.post('/edit-password')
async def edit_password(
    password_in: EditPasswordSchema,
    current_user: User = Depends(get_current_user),
):
    await user_service.change_password(
        user=current_user,
        old_password=password_in.old_password,
        new_password=password_in.new_password,
    )
    return SuccessResponse(data={"msg": "修改密码成功"})


@router.post('/reset-password')
async def reset_password(
    user_id: int,
    current_user: User = Security(permission_check, scopes=['user:reset-password']),
):
    username, new_password = await user_service.reset_password(user_id=user_id)
    return SuccessResponse(data={"new_password": new_password})
