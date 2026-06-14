from typing import Optional, List, Tuple

from tortoise.expressions import Q

from shared.base_repository import BaseRepository
from modules.system.models import User, Role, Menu


class UserRepository(BaseRepository[User]):
    model_class = User

    async def find_by_username(self, username: str) -> Optional[User]:
        return await User.get_or_none(username=username)

    async def list_paginated(
        self,
        current: int = 1,
        size: int = 10,
        username: Optional[str] = None,
        phone: Optional[str] = None,
        email: Optional[str] = None,
    ) -> Tuple[List[User], int]:
        query = User.all()
        if username:
            query = query.filter(username__contains=username)
        if phone:
            query = query.filter(phone__contains=phone)
        if email:
            query = query.filter(email__contains=email)

        total = await query.count()
        users = await query.offset((current - 1) * size).limit(size).prefetch_related("roles").all()
        return list(users), total


class RoleRepository(BaseRepository[Role]):
    model_class = Role

    async def find_by_code(self, code: str) -> Optional[Role]:
        return await Role.get_or_none(code=code)

    async def find_by_codes(self, codes: List[str]) -> List[Role]:
        return await Role.filter(code__in=codes)

    async def list_paginated(
        self,
        current: int = 1,
        size: int = 10,
        name: Optional[str] = None,
        code: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Tuple[List[Role], int]:
        query = Role.all()
        if name:
            query = query.filter(name__contains=name)
        if code:
            query = query.filter(code__contains=code)
        if description:
            query = query.filter(description__contains=description)

        total = await query.count()
        roles = await query.offset((current - 1) * size).limit(size).all()
        return list(roles), total

    async def find_by_name_or_code(self, name: str, code: str) -> Optional[Role]:
        return await Role.filter(Q(name=name) | Q(code=code)).first()


class MenuRepository(BaseRepository[Menu]):
    model_class = Menu

    async def get_all_sorted(self) -> List[Menu]:
        return await Menu.filter().order_by("sort").all()

    async def get_by_ids(self, ids: List[int]) -> List[Menu]:
        if not ids:
            return []
        return await Menu.filter(id__in=ids)

    async def delete_children(self, parent_id: int) -> None:
        await Menu.filter(parent_id=parent_id).delete()


# 单例实例
user_repo = UserRepository(User)
role_repo = RoleRepository(Role)
menu_repo = MenuRepository(Menu)
