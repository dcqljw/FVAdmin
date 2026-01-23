import os.path
import random
import string

from fastapi import APIRouter, Depends, Security, UploadFile

from core.security import get_password_hash, verify_password
from core.settings import settings
from models.menu_model import Menu
from models.user_model import User, UserPydantic, UserPydanticList, UserResponse
from models.role_model import Role, RolePydantic, RolePydanticList
from oss_client import oss_client
from router.deps import verify_token_dep, get_current_user, permission_check
from schemas.response import SuccessResponse, ErrorResponse
from schemas.user import UserCreateSchema, EditPasswordSchema
from schemas.role import RoleCreateSchema, RoleMenuCreateSchema
from core.log_config import api_logger

router = APIRouter(prefix="/user", tags=["用户管理"])


@router.get("/info")
async def get_user_info(user: User = Depends(get_current_user)):
    api_logger.info(f"用户 {user.username} 查询个人信息")
    user_data = UserResponse.model_validate(user)
    user_dict = user_data.model_dump(mode="json")
    api_logger.info(f"用户 {user.username} 查询个人信息成功")
    return SuccessResponse(data=user_dict)


@router.get("/list")
async def get_user(user: User = Depends(get_current_user),
                   current: int = 1,
                   size: int = 10,
                   username: str = None,
                   phone: str = None,
                   email: str = None,
                   ):
    api_logger.info(
        f"用户 {user.username} 查询用户列表，参数：page={current}, size={size}, username={username}, phone={phone}, email={email}")
    query = User.all()
    if username:
        query = query.filter(username__contains=username)
    if phone:
        query = query.filter(phone__contains=phone)
    if email:
        query = query.filter(email__contains=email)
    user_roles_model = await query.offset((current - 1) * size).limit(
        size).all().prefetch_related("roles")
    user_list = UserPydanticList(root=user_roles_model).model_dump(mode='json')['root']
    for idx, user_obj in enumerate(user_roles_model):
        user_list[idx]['roles'] = [i.code for i in user_obj.roles]
    api_logger.info(f"用户 {user.username} 查询用户列表成功，返回 {len(user_list)} 条记录")
    return SuccessResponse(data=user_list)


@router.post("/add")
async def add_user(user: UserCreateSchema, current_user: User = Security(permission_check, scopes=['user:add'])):
    api_logger.info(f"用户 {current_user.username} 尝试添加新用户 {user.username}")
    is_user = await User.get_or_none(username=user.username)
    if is_user:
        api_logger.warning(f"添加用户失败：用户名 {user.username} 已存在")
        return ErrorResponse(message="用户已存在")
    else:
        user.password = get_password_hash(user.password)
        role = await Role.filter(code__in=user.role)
        create_user = await User.create(**user.model_dump())
        await create_user.roles.add(*role)
        api_logger.info(f"用户 {current_user.username} 成功添加用户 {user.username}")
        return SuccessResponse(data={"msg": "添加用户成功"})


@router.post('/edit')
async def edit_user(user_in: UserCreateSchema, current_user: User = Security(permission_check, scopes=['user:edit'])):
    api_logger.info(f"用户 {current_user.username} 尝试编辑用户信息 {user_in.username}")
    user = await User.get_or_none(username=user_in.username)
    if user:
        user.nickname = user_in.nickname
        user.phone = user_in.phone
        user.email = user_in.email
        user.avatar = user_in.avatar
        await user.roles.clear()
        await user.save()
        role = await Role.filter(code__in=user_in.role)
        await user.roles.add(*role)
        api_logger.info(f"用户 {current_user.username} 成功编辑用户信息 {user_in.username}")
        return SuccessResponse(data={"msg": "修改用户成功"})
    else:
        api_logger.warning(f"编辑用户失败：用户 {user_in.username} 不存在")
        return ErrorResponse(message="用户不存在")


@router.post('/edit-profile')
async def edit_profile(user_in: UserCreateSchema, current_user: User = Depends(get_current_user)):
    api_logger.info(f"用户 {current_user.username} 尝试修改个人资料")
    user = await User.get_or_none(username=current_user.username)
    if user:
        user.nickname = user_in.nickname
        user.phone = user_in.phone
        user.email = user_in.email
        user.avatar = user_in.avatar
        await user.save()
        api_logger.info(f"用户 {current_user.username} 成功修改个人资料")
        return SuccessResponse(data={"msg": "修改用户成功"})


@router.post('/upload_avatar')
async def upload_avatar(file: UploadFile, current_user: User = Depends(get_current_user)):
    api_logger.info(f"用户 {current_user.username} 尝试上传头像")
    if file.content_type not in ["image/jpeg", "image/png"]:
        api_logger.warning(f"用户 {current_user.username} 上传头像失败：文件类型不支持")
        return ErrorResponse(message="请上传图片")
    if file.size > 1 * 1024 * 1024:
        api_logger.warning(f"用户 {current_user.username} 上传头像失败：文件过大")
        return ErrorResponse(message="请上传1MB以内的文件")
    file_ext = os.path.splitext(file.filename)[-1]
    filename = oss_client.get_md5(file.file.read()) + f"{file_ext}"
    oss_client.upload_file_by_stream(file.file, filename, extra_args={"ContentType": file.content_type})
    current_user.avatar = f"{settings.OSS_URL}/{settings.OSS_BUCKET}/{filename}"
    await current_user.save()
    api_logger.info(f"用户 {current_user.username} 成功上传头像")
    return SuccessResponse(data={"msg": "上传成功"})


@router.post('/delete')
async def delete_user(user_id: int, current_user: User = Security(permission_check, scopes=['user:delete'])):
    api_logger.info(f"用户 {current_user.username} 尝试删除用户ID {user_id}")
    if user_id == current_user.id:
        api_logger.warning(f"用户 {current_user.username} 尝试删除自己，操作被拒绝")
        return ErrorResponse(message="不能删除自己")
    user = await User.get_or_none(id=user_id)
    if user.username == "admin":
        api_logger.warning(f"用户 {current_user.username} 尝试删除管理员账户，操作被拒绝")
        return ErrorResponse(message="超级管理员无法删除")
    if user:
        await user.delete()
        api_logger.info(f"用户 {current_user.username} 成功删除用户 {user.username}")
        return SuccessResponse(data={"msg": "删除用户成功"})
    else:
        api_logger.warning(f"删除用户失败：用户ID {user_id} 不存在")
        return ErrorResponse(message="用户不存在")


@router.post('/edit-password')
async def edit_password(password_in: EditPasswordSchema, current_user: User = Depends(get_current_user)):
    api_logger.info(f"用户 {current_user.username} 尝试修改密码")
    user_data = await User.get_or_none(username=current_user.username)
    if user_data:
        if verify_password(password_in.old_password, user_data.password):
            password = get_password_hash(password_in.new_password)
            user_data.password = password
            await user_data.save()
            api_logger.info(f"用户 {current_user.username} 成功修改密码")
            return SuccessResponse(data={"msg": "修改密码成功"})
        else:
            api_logger.warning(f"用户 {current_user.username} 修改密码失败：原密码错误")
            return ErrorResponse(message="原密码错误")
    else:
        api_logger.error(f"修改密码异常：用户 {current_user.username} 数据不一致")
        return ErrorResponse(message="原密码错误")


@router.post('/reset-password')
async def reset_password(user_id: int, current_user: User = Security(permission_check, scopes=['user:reset-password'])):
    api_logger.info(f"用户 {current_user.username} 尝试重置用户ID {user_id} 的密码")
    user = await User.get_or_none(id=user_id)
    if user:
        random_str = string.ascii_lowercase + string.ascii_uppercase + string.digits
        new_password = "".join(random.choices(random_str, k=8))
        user.password = get_password_hash(new_password)
        await user.save()
        api_logger.info(f"用户 {current_user.username} 成功重置用户 {user.username} 的密码")
        return SuccessResponse(data={"new_password": new_password})
    else:
        api_logger.warning(f"重置密码失败：用户ID {user_id} 不存在")
        return ErrorResponse(message="用户不存在")
