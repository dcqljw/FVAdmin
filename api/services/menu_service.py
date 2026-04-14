from typing import List

from tortoise.functions import Count

from core.log_config import api_logger
from core.util import convert_menu_to_tree
from custom_exception import CustomException
from models.menu_model import Menu, MenuPydanticList
from models.role_model import Role
from services.base import BaseService


class MenuService(BaseService):

    async def get_menu_tree_for_user(self, user) -> List[dict]:
        all_menus = []
        if user.username == "admin":
            all_menus = await Menu.filter().order_by("-sort").all()
        else:
            roles = await user.roles.all()
            for role in roles:
                role_menus = await role.menus.order_by("-sort")
                all_menus.extend(role_menus)

        pydantic_list = MenuPydanticList(all_menus).model_dump(mode="json")
        return convert_menu_to_tree(pydantic_list)

    async def get_role_leaf_menu_ids(self, role_id: int) -> List[int]:
        try:
            role = await Role.get(id=role_id).prefetch_related("menus")
        except Exception:
            return []

        selected_menus = await role.menus.all()
        if not selected_menus:
            return []

        selected_menu_ids = [menu.id for menu in selected_menus]

        child_count_map = (
            await Menu.filter(parent_id__in=selected_menu_ids)
            .annotate(count=Count("id"))
            .group_by("parent_id")
            .values("parent_id", "count")
        )

        count_dict = {item["parent_id"]: item["count"] for item in child_count_map}

        return [
            menu_id for menu_id in selected_menu_ids
            if count_dict.get(menu_id, 0) == 0
        ]

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
        menu = await Menu.create(
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
        name: str,
        path: str,
        meta: dict,
        component: str,
        sort: int,
        status: bool,
        auth_mark: str,
        menu_type: int,
    ) -> Menu:
        menu = await Menu.get_or_none(name=name)
        if not menu:
            self._not_found("菜单", name)

        if menu_type == 1:
            menu.name = name
            menu.path = path
            menu.meta = meta
            menu.component = component
            menu.sort = sort
            menu.status = status
        else:
            menu.name = name
            menu.meta = meta
            menu.auth_mark = auth_mark

        await menu.save()
        api_logger.info(f"成功更新菜单: {name}")
        return menu

    async def delete_menu(self, menu_id: int) -> str:
        menu = await Menu.get_or_none(id=menu_id)
        if not menu:
            self._not_found("菜单", str(menu_id))

        if menu.name == "Menus":
            self._forbidden("不能删除根菜单")

        deleted_name = menu.name
        await Menu.filter(parent_id=menu_id).delete()
        await menu.delete()

        api_logger.info(f"成功删除菜单: {deleted_name}")
        return deleted_name

    async def assign_menus_to_role(
        self, role_id: int, menu_ids: List[int]
    ) -> Role:
        role = await Role.get(id=role_id)
        await role.menus.clear()
        menus = await Menu.filter(id__in=menu_ids)
        await role.menus.add(*menus)

        api_logger.info(f"成功为角色ID {role_id} 分配菜单权限")
        return role


menu_service = MenuService()
