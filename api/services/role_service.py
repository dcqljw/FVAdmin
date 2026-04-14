from typing import Optional

from tortoise.expressions import Q

from core.log_config import api_logger
from custom_exception import CustomException
from models.role_model import Role, RoleResponse, RoleListResponse
from models.user_model import User
from services.base import BaseService


class RoleService(BaseService):

    async def list_roles(
        self,
        current: int = 1,
        size: int = 10,
        name: Optional[str] = None,
        code: Optional[str] = None,
        description: Optional[str] = None,
    ) -> RoleListResponse:
        query = Role.all()
        if name:
            query = query.filter(name__contains=name)
        if code:
            query = query.filter(code__contains=code)
        if description:
            query = query.filter(description__contains=description)

        roles = await query.offset((current - 1) * size).limit(size).all()
        role_response = [RoleResponse.model_validate(role) for role in roles]
        return RoleListResponse(data=role_response)

    async def create_role(
        self, name: str, code: str, description: str, enabled: bool
    ) -> Role:
        existing = await Role.filter(Q(name=name) | Q(code=code)).first()
        if existing:
            self._already_exists("角色", f"{name} 或 {code}")

        role = await Role.create(
            name=name, code=code, description=description, enabled=enabled
        )
        api_logger.info(f"成功创建角色: {name}")
        return role

    async def delete_role(self, role_id: int, current_user: User) -> str:
        if role_id == current_user.id:
            self._forbidden("不能删除自己")

        role = await Role.get_or_none(id=role_id)
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
        role = await Role.get_or_none(code=code)
        if not role:
            self._not_found("角色", code)

        role.name = name
        role.description = description
        role.enabled = enabled
        await role.save()

        api_logger.info(f"成功更新角色: {code}")
        return role


role_service = RoleService()
