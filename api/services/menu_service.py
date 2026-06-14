from typing import List

from core.log_config import api_logger
from core.util import convert_menu_to_tree
from models.menu_model import Menu, MenuPydanticList
from models.role_model import Role
from services.base import BaseService


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
        menus = await Menu.filter().order_by("sort").all()
        return self._menus_to_tree(menus)

    async def get_user_menu_tree(self, user) -> List[dict]:
        """
        获取用户有权限的菜单树（侧边栏导航使用）
        - admin：返回全部
        - 普通用户：按角色关联的菜单过滤，并自动补全祖先链，防止父菜单未分配时子菜单消失
        """
        if user.username == "admin":
            menus = await Menu.filter().order_by("sort").all()
        else:
            roles = await user.roles.all().prefetch_related("menus")
            direct_ids: set[int] = set()
            for role in roles:
                for menu in role.menus:
                    direct_ids.add(menu.id)

            if not direct_ids:
                return []

            # 一次查出所有菜单，在内存中构建 parent 映射，避免逐级 DB 查询
            all_menus = await Menu.filter().order_by("sort").all()
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
        menu = await Menu.get_or_none(id=menu_id)
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
