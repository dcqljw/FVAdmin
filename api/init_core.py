import random
import string

from core.security import get_password_hash
from models.menu_model import Menu
from models.role_model import Role
from models.user_model import User


async def create_superuser():
    user = await User.get_or_none(username="admin")
    if not user:
        print("创建超级管理员")
        random_str = string.ascii_lowercase + string.ascii_uppercase + string.digits
        password = "".join(random.choices(random_str, k=8))
        print(f"密码：{password}")
        new_password = get_password_hash(password)
        await User.create(username="admin", password=new_password, nickname="管理员", phone="12345678901",
                          email="admin@admin.com", avatar='')


async def create_menu():
    menus = await Menu.filter().all()
    if menus:
        return
    # 创建父级菜单
    dashboard_menu = await Menu.create(
        parent_id=0, name="Dashboard", path="/dashboard",
        meta={"icon": "ri:pie-chart-line", "title": "menus.dashboard.title"}, component="/index/index", sort=1,
        auth_mark="dashboard",
        type=1
    )
    system_menu = await Menu.create(
        parent_id=0, name="System", path="/system",
        meta={"icon": "ri:settings-line", "title": "系统管理"}, component="/index/index", sort=2,
        auth_mark="system",
        type=1
    )
    # 创建子级菜单

    await Menu.create(parent_id=dashboard_menu.id, name="Console", path="console",
                      meta={"icon": "ri:home-smile-2-line", "title": "工作台"}, component="/dashboard/console", sort=1,
                      auth_mark="console",
                      type=1)
    await Menu.create(parent_id=system_menu.id, name="UserCenter", path="user-center",
                      meta={"icon": "ri:user-line", "title": "menus.system.userCenter", "isHide": True,
                            "isHideTab": True, "keepAlive": True}, component="/system/user-center", sort=1,
                      auth_mark="user-center",
                      type=1)
    user_menu = await Menu.create(parent_id=system_menu.id, name="User", path="user",
                                  meta={"icon": "ri:user-line", "title": "menus.system.user", "keepAlive": True},
                                  component="/system/user",
                                  sort=1,
                                  auth_mark="user", type=1)

    user_auth_mark_list = [
        Menu(parent_id=user_menu.id, name="", path="",
             meta={"title": "新增"}, component="",
             sort=1,
             auth_mark="user:add", type=2),
        Menu(parent_id=user_menu.id, name="", path="",
             meta={"title": "删除"}, component="",
             sort=1,
             auth_mark="user:delete", type=2),
        Menu(parent_id=user_menu.id, name="", path="",
             meta={"title": "修改"}, component="",
             sort=1,
             auth_mark="user:edit", type=2),
        Menu(parent_id=user_menu.id, name="", path="",
             meta={"title": "重置密码"}, component="",
             sort=1,
             auth_mark="user:reset-password", type=2),
    ]
    await Menu.bulk_create(user_auth_mark_list)

    role_menu = await Menu.create(parent_id=system_menu.id, name="Role", path="role",
                                  meta={"icon": "ri:user-settings-line", "title": "角色管理"}, component="/system/role",
                                  sort=1,
                                  auth_mark="role", type=1)
    role_auth_mark_list = [
        Menu(parent_id=role_menu.id, name="", path="",
             meta={"title": "新增"}, component="",
             sort=1,
             auth_mark="role:add", type=2),
        Menu(parent_id=role_menu.id, name="", path="",
             meta={"title": "删除"}, component="",
             sort=1,
             auth_mark="role:delete", type=2),
        Menu(parent_id=role_menu.id, name="", path="",
             meta={"title": "修改"}, component="",
             sort=1,
             auth_mark="role:edit", type=2),
    ]
    await Menu.bulk_create(role_auth_mark_list)

    menu_menu = await Menu.create(parent_id=system_menu.id, name="Menu", path="menu",
                                  meta={"icon": "ri:menu-line", "title": "菜单管理"}, component="/system/menu",
                                  sort=1,
                                  auth_mark="menu:list", type=1)
    menu_auth_mark_list = [
        Menu(parent_id=menu_menu.id, name="添加菜单", path="",
             meta={"title": "添加菜单"}, component="",
             sort=1,
             auth_mark="menu:add", type=2),
        Menu(parent_id=menu_menu.id, name="删除菜单", path="",
             meta={"title": "删除菜单"}, component="",
             sort=1,
             auth_mark="menu:delete", type=2),
        Menu(parent_id=menu_menu.id, name="编辑菜单", path="",
             meta={"title": "编辑菜单"}, component="",
             sort=1,
             auth_mark="menu:edit", type=2),
    ]
    await Menu.bulk_create(menu_auth_mark_list)


async def create_role():
    role = await Role.get_or_none(name="admin")
    if not role:
        print("创建超级管理员角色")
        admin_role = await Role.create(name="admin", code="ADMIN", description="超级管理员", enabled=True)
        await admin_role.menus.add(*await Menu.all())
        user = await User.filter(username="admin").first()
        await user.roles.add(admin_role)


async def init_data():
    await create_superuser()
    await create_menu()
    await create_role()
