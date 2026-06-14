import os.path
import random
import string
from io import BytesIO
from typing import List, Optional, Tuple

from shared.base_service import BaseService
from shared.log_config import api_logger
from shared.oss_client import oss_client
from shared.utils import convert_menu_to_tree
from core.security import get_password_hash, verify_password
from core.config import settings
from core.exceptions import CustomException
from modules.system.models import User, Role, Menu, UserResponse, RoleResponse, MenuPydanticList
from modules.system.repository import user_repo, role_repo, menu_repo


# ========== SystemPublicService ==========
# 跨模块公共 API：供其他模块（如 auth）调用，避免直接 import system 内部 repository / models

class SystemPublicService:
    """system 模块对外暴露的公共服务，其他模块通过此类访问 system 数据"""

    @staticmethod
    async def verify_credentials(username: str, password: str) -> Optional[User]:
        """
        校验用户名密码，成功返回 User，失败返回 None。
        把"按用户名查找 + bcrypt 校验"封装在 system 模块内部，
        外部模块（如 auth）无需接触 UserRepository / verify_password。
        """
        user = await user_repo.find_by_username(username)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user


# ========== UserService ==========

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
        role_id: Optional[int] = None,
    ) -> Tuple[List[dict], int]:
        users, total = await user_repo.list_paginated(
            current=current, size=size,
            username=username, phone=phone, email=email,
            role_id=role_id,
        )

        records = []
        for u in users:
            data = UserResponse.model_validate(u).model_dump(mode="json")
            data["roles"] = [r.code for r in u.roles]
            records.append(data)
        return records, total

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
        existing = await user_repo.find_by_username(username)
        if existing:
            self._already_exists("用户", username)

        hashed_password = get_password_hash(password)
        user = await user_repo.create(
            username=username,
            password=hashed_password,
            nickname=nickname,
            email=email or "",
            phone=phone or "",
            avatar=avatar or "",
        )
        roles = await role_repo.find_by_codes(role_codes)
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
        user = await user_repo.find_by_username(username)
        if not user:
            self._not_found("用户", username)

        user.nickname = nickname
        user.phone = phone or ""
        user.email = email or ""
        user.avatar = avatar or ""
        await user.save()

        await user.roles.clear()
        roles = await role_repo.find_by_codes(role_codes)
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

        user = await user_repo.get_by_id(user_id)
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
        user = await user_repo.get_by_id(user_id)
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


# ========== RoleService ==========

class RoleService(BaseService):

    async def list_roles(
        self,
        current: int = 1,
        size: int = 10,
        name: Optional[str] = None,
        code: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Tuple[List[dict], int]:
        roles, total = await role_repo.list_paginated(
            current=current, size=size,
            name=name, code=code, description=description,
        )
        role_list = [RoleResponse.model_validate(role).model_dump(mode="json") for role in roles]
        return role_list, total

    async def create_role(
        self, name: str, code: str, description: str, enabled: bool
    ) -> Role:
        existing = await role_repo.find_by_name_or_code(name, code)
        if existing:
            self._already_exists("角色", f"{name} 或 {code}")

        role = await role_repo.create(
            name=name, code=code, description=description, enabled=enabled
        )
        api_logger.info(f"成功创建角色: {name}")
        return role

    async def delete_role(self, role_id: int, current_user: User) -> str:
        if role_id == current_user.id:
            self._forbidden("不能删除自己")

        role = await role_repo.get_by_id(role_id)
        if not role:
            self._not_found("角色", str(role_id))

        if role.code == "R_ADMIN":
            self._forbidden("超级管理员无法删除")

        deleted_name = role.name
        await role.delete()

        api_logger.info(f"成功删除角色: {deleted_name}")
        return deleted_name

    async def update_role(
        self, code: str, name: str, description: str, enabled: bool
    ) -> Role:
        role = await role_repo.find_by_code(code)
        if not role:
            self._not_found("角色", code)

        role.name = name
        role.description = description
        role.enabled = enabled
        await role.save()

        api_logger.info(f"成功更新角色: {code}")
        return role


# ========== MenuService ==========

class MenuService(BaseService):

    @staticmethod
    def _menus_to_tree(menus) -> List[dict]:
        """把 Menu 列表序列化成前端需要的树形结构"""
        if not menus:
            return []
        pydantic_list = MenuPydanticList(menus).model_dump(mode="json")
        return convert_menu_to_tree(pydantic_list)

    async def get_all_menu_tree(self) -> List[dict]:
        """
        获取全量菜单树（菜单管理页使用）
        返回所有菜单，含 type=1（菜单）和 type=2（按钮）
        """
        menus = await menu_repo.get_all_sorted()
        return self._menus_to_tree(menus)

    async def get_user_menu_tree(self, user) -> List[dict]:
        """
        获取用户有权限的菜单树（侧边栏导航使用）
        - admin：返回全部
        - 普通用户：按角色关联的菜单过滤，并自动补全祖先链，防止父菜单未分配时子菜单消失
        """
        if user.username == "admin":
            menus = await menu_repo.get_all_sorted()
        else:
            roles = await user.roles.all().prefetch_related("menus")
            direct_ids: set[int] = set()
            for role in roles:
                for menu in role.menus:
                    direct_ids.add(menu.id)

            if not direct_ids:
                return []

            # 一次查出所有菜单，在内存中构建 parent 映射，避免逐级 DB 查询
            all_menus = await menu_repo.get_all_sorted()
            menu_map = {m.id: m for m in all_menus}

            # 从直接权限点向上补全所有祖先节点（parent_id 为 0/None 表示根，已被 falsy 排除）
            complete_ids = set(direct_ids)
            queue = list(direct_ids)
            while queue:
                mid = queue.pop()
                m = menu_map.get(mid)
                if m and m.parent_id and m.parent_id not in complete_ids:
                    complete_ids.add(m.parent_id)
                    queue.append(m.parent_id)

            menus = [m for m in all_menus if m.id in complete_ids]

        return self._menus_to_tree(menus)

    async def get_role_menu_ids(self, role_id: int) -> List[int]:
        """
        返回角色关联的全部菜单/权限 ID（直接读中间表，不做叶子过滤）
        前端 applyCheckedIds 已负责在树中还原勾选和半选状态
        """
        try:
            role = await Role.get(id=role_id)
        except Exception:
            return []

        selected_menus = await role.menus.all()
        return [menu.id for menu in selected_menus]

    async def create_menu(
        self,
        parent_id: int,
        name: str,
        path: str,
        meta: dict,
        component: str,
        sort: int,
        status: bool,
        auth_mark: str,
        menu_type: int,
    ) -> Menu:
        menu = await menu_repo.create(
            parent_id=parent_id,
            name=name,
            path=path,
            meta=meta,
            component=component,
            sort=sort,
            status=status,
            auth_mark=auth_mark,
            type=menu_type,
        )
        api_logger.info(f"成功创建菜单: {name}")
        return menu

    async def update_menu(
        self,
        menu_id: int,
        name: str,
        path: str,
        meta: dict,
        component: str,
        sort: int,
        status: bool,
        auth_mark: str,
        menu_type: int,
    ) -> Menu:
        menu = await menu_repo.get_by_id(menu_id)
        if not menu:
            self._not_found("菜单", str(menu_id))

        # 菜单与按钮共享的字段
        menu.name = name
        menu.meta = meta
        menu.sort = sort

        if menu_type == 1:
            menu.path = path
            menu.component = component
            menu.status = status
        else:
            menu.auth_mark = auth_mark

        await menu.save()
        api_logger.info(f"成功更新菜单: {name}")
        return menu

    async def delete_menu(self, menu_id: int) -> str:
        menu = await menu_repo.get_by_id(menu_id)
        if not menu:
            self._not_found("菜单", str(menu_id))

        if menu.name == "Menus":
            self._forbidden("不能删除根菜单")

        deleted_name = menu.name
        await menu_repo.delete_children(menu_id)
        await menu.delete()

        api_logger.info(f"成功删除菜单: {deleted_name}")
        return deleted_name

    async def assign_menus_to_role(
        self, role_id: int, menu_ids: List[int]
    ) -> Role:
        role = await Role.get(id=role_id)
        await role.menus.clear()
        menus = await menu_repo.get_by_ids(menu_ids)
        await role.menus.add(*menus)

        api_logger.info(f"成功为角色ID {role_id} 分配菜单权限")
        return role


# 单例实例
system_public_service = SystemPublicService()
user_service = UserService()
role_service = RoleService()
menu_service = MenuService()
