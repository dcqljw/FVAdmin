import os.path
import random
import string
from io import BytesIO
from typing import List, Optional, Tuple

from core.log_config import api_logger
from core.security import get_password_hash, verify_password
from core.settings import settings
from custom_exception import CustomException
from models.role_model import Role
from models.user_model import User, UserResponse, UserPydanticList
from oss_client import oss_client
from services.base import BaseService


class UserService(BaseService):

    async def get_user_info(self, user: User) -> dict:
        user_data = UserResponse.model_validate(user)
        return user_data.model_dump(mode="json")

    async def list_users(
        self,
        current: int = 1,
        size: int = 10,
        username: Optional[str] = None,
        phone: Optional[str] = None,
        email: Optional[str] = None,
    ) -> Tuple[List[dict], int]:
        query = User.all()
        if username:
            query = query.filter(username__contains=username)
        if phone:
            query = query.filter(phone__contains=phone)
        if email:
            query = query.filter(email__contains=email)

        total = await query.count()
        users = await query.offset((current - 1) * size).limit(size).prefetch_related("roles").all()

        user_list = UserPydanticList(root=users).model_dump(mode="json")["root"]
        for idx, user_obj in enumerate(users):
            user_list[idx]["roles"] = [role.code for role in user_obj.roles]

        return user_list, total

    async def create_user(
        self,
        username: str,
        password: str,
        nickname: str,
        role_codes: List[str],
        email: Optional[str] = None,
        phone: Optional[str] = None,
        avatar: Optional[str] = None,
    ) -> User:
        existing = await User.get_or_none(username=username)
        if existing:
            self._already_exists("用户", username)

        hashed_password = get_password_hash(password)
        user = await User.create(
            username=username,
            password=hashed_password,
            nickname=nickname,
            email=email or "",
            phone=phone or "",
            avatar=avatar or "",
        )
        roles = await Role.filter(code__in=role_codes)
        await user.roles.add(*roles)

        api_logger.info(f"成功创建用户: {username}")
        return user

    async def update_user(
        self,
        username: str,
        nickname: str,
        role_codes: List[str],
        email: Optional[str] = None,
        phone: Optional[str] = None,
        avatar: Optional[str] = None,
    ) -> User:
        user = await User.get_or_none(username=username)
        if not user:
            self._not_found("用户", username)

        user.nickname = nickname
        user.phone = phone or ""
        user.email = email or ""
        user.avatar = avatar or ""
        await user.save()

        await user.roles.clear()
        roles = await Role.filter(code__in=role_codes)
        await user.roles.add(*roles)

        api_logger.info(f"成功更新用户: {username}")
        return user

    async def update_profile(
        self,
        user: User,
        nickname: str,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        avatar: Optional[str] = None,
    ) -> User:
        user.nickname = nickname
        user.phone = phone or ""
        user.email = email or ""
        user.avatar = avatar or ""
        await user.save()

        api_logger.info(f"用户 {user.username} 成功修改个人资料")
        return user

    async def delete_user(self, user_id: int, current_user: User) -> str:
        if user_id == current_user.id:
            self._forbidden("不能删除自己")

        user = await User.get_or_none(id=user_id)
        if not user:
            self._not_found("用户", str(user_id))

        if user.username == "admin":
            self._forbidden("超级管理员无法删除")

        deleted_username = user.username
        await user.delete()

        api_logger.info(f"成功删除用户: {deleted_username}")
        return deleted_username

    async def change_password(
        self, user: User, old_password: str, new_password: str
    ) -> User:
        if not verify_password(old_password, user.password):
            raise CustomException(code=400, msg="原密码错误")

        user.password = get_password_hash(new_password)
        await user.save()

        api_logger.info(f"用户 {user.username} 成功修改密码")
        return user

    async def reset_password(self, user_id: int) -> Tuple[str, str]:
        user = await User.get_or_none(id=user_id)
        if not user:
            self._not_found("用户", str(user_id))

        random_str = string.ascii_lowercase + string.ascii_uppercase + string.digits
        new_password = "".join(random.choices(random_str, k=8))
        user.password = get_password_hash(new_password)
        await user.save()

        api_logger.info(f"成功重置用户 {user.username} 的密码")
        return user.username, new_password

    async def upload_avatar(
        self, user: User, file_content: bytes, filename: str,
        content_type: str, file_size: int
    ) -> str:
        allowed_types = ["image/jpeg", "image/png"]
        if content_type not in allowed_types:
            raise CustomException(code=400, msg="请上传图片")

        max_size = 1 * 1024 * 1024
        if file_size > max_size:
            raise CustomException(code=400, msg="请上传1MB以内的文件")

        file_ext = os.path.splitext(filename)[-1]
        file_md5 = oss_client.get_md5(file_content)
        oss_filename = file_md5 + file_ext

        file_obj = BytesIO(file_content)
        oss_client.upload_file_by_stream(
            file_obj, oss_filename, extra_args={"ContentType": content_type}
        )

        avatar_url = f"{settings.OSS_URL}/{settings.OSS_BUCKET}/{oss_filename}"
        user.avatar = avatar_url
        await user.save()

        api_logger.info(f"用户 {user.username} 成功上传头像")
        return avatar_url


user_service = UserService()
