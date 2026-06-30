"""
数据初始化脚本

使用方式（需先执行 aerich upgrade 确保表结构就绪）：
    uv run python seed.py

幂等：重复执行不会重复插入数据（按 auth_mark / code 判断是否存在）
"""

import asyncio
from typing import Any

from tortoise import Tortoise

from core.db import db_config
from modules.system.models import Menu, Role
from shared.log_config import app_logger


# ── 菜单种子数据 ──────────────────────────────────────────────
# 用 auth_mark 作为唯一标识判断是否已存在
# type 默认为 1（菜单），按钮需显式指定 type=2
SEED_MENUS: list[dict[str, Any]] = [
    # 顶级菜单
    {
        "name": "Dashboard", "path": "/dashboard",
        "auth_mark": "dashboard",
        "meta": {"icon": "ri:pie-chart-line", "title": "menus.dashboard.title"},
        "sort": 1, "component": "/index/index",
    },
    {
        "name": "System", "path": "/system",
        "auth_mark": "system",
        "meta": {"icon": "ri:settings-line", "title": "系统管理"},
        "sort": 2, "component": "/index/index",
    },
    {
        "name": "AI", "path": "/ai",
        "auth_mark": "ai",
        "meta": {"icon": "ri:robot-line", "title": "AI 能力"},
        "sort": 3, "component": "/index/index",
    },

    # Dashboard 子菜单
    {
        "parent_auth_mark": "dashboard",
        "name": "Console", "path": "console",
        "auth_mark": "console",
        "meta": {"icon": "ri:home-smile-2-line", "title": "工作台"},
        "sort": 1, "component": "/dashboard/console",
    },

    # System 子菜单
    {
        "parent_auth_mark": "system",
        "name": "UserCenter", "path": "user-center",
        "auth_mark": "user-center",
        "meta": {"icon": "ri:user-line", "title": "menus.system.userCenter",
                 "isHide": True, "isHideTab": True, "keepAlive": True},
        "sort": 1, "component": "/system/user-center",
    },
    {
        "parent_auth_mark": "system",
        "name": "User", "path": "user",
        "auth_mark": "user",
        "meta": {"icon": "ri:user-line", "title": "menus.system.user", "keepAlive": True},
        "sort": 2, "component": "/system/user",
    },
    {
        "parent_auth_mark": "system",
        "name": "Role", "path": "role",
        "auth_mark": "role",
        "meta": {"icon": "ri:user-settings-line", "title": "角色管理"},
        "sort": 3, "component": "/system/role",
    },
    {
        "parent_auth_mark": "system",
        "name": "Menu", "path": "menu",
        "auth_mark": "system:menu",
        "meta": {"icon": "ri:menu-line", "title": "菜单管理"},
        "sort": 4, "component": "/system/menu",
    },

    # AI 子菜单
    {
        "parent_auth_mark": "ai",
        "name": "MCP Server", "path": "mcp-server",
        "auth_mark": "ai:mcp",
        "meta": {"icon": "ri:server-line", "title": "MCP 服务器"},
        "sort": 1, "component": "/ai/mcp-server",
    },
    {
        "parent_auth_mark": "ai",
        "name": "Chat", "path": "chat",
        "auth_mark": "chat",
        "meta": {"icon": "ri:chat-3-line", "title": "AI 对话"},
        "sort": 2, "component": "/chat/index",
    },
    {
        "parent_auth_mark": "ai",
        "name": "LLM Model", "path": "llm-model",
        "auth_mark": "model",
        "meta": {"icon": "ri:brain-line", "title": "模型管理"},
        "sort": 3, "component": "/model/index",
    },
]

# 按钮权限：(parent_auth_mark, auth_mark, title, sort)
_SEED_BUTTONS: list[tuple[str, str, str, int]] = [
    # User 按钮
    ("user", "system:user:list", "列表", 1),
    ("user", "system:user:add", "新增", 2),
    ("user", "system:user:edit", "修改", 3),
    ("user", "system:user:delete", "删除", 4),
    ("user", "user:reset-password", "重置密码", 5),
    # Role 按钮
    ("role", "system:role:list", "列表", 1),
    ("role", "system:role:add", "新增", 2),
    ("role", "system:role:edit", "修改", 3),
    ("role", "system:role:delete", "删除", 4),
    # Menu 按钮
    ("system:menu", "system:menu:list", "列表", 1),
    ("system:menu", "system:menu:add", "新增", 2),
    ("system:menu", "system:menu:edit", "修改", 3),
    ("system:menu", "system:menu:delete", "删除", 4),
    # MCP Server 按钮
    ("ai:mcp", "ai:mcp:list", "列表", 1),
    ("ai:mcp", "ai:mcp:add", "新增", 2),
    ("ai:mcp", "ai:mcp:edit", "修改", 3),
    ("ai:mcp", "ai:mcp:delete", "删除", 4),
    # Chat 按钮
    ("chat", "chat:session:list", "会话列表", 1),
    ("chat", "chat:session:create", "创建会话", 2),
    ("chat", "chat:session:delete", "删除会话", 3),
    ("chat", "chat:message:list", "消息列表", 4),
    ("chat", "chat:message:send", "发送消息", 5),
    # LLM Model 按钮
    ("model", "model:list", "列表", 1),
    ("model", "model:add", "新增", 2),
    ("model", "model:edit", "修改", 3),
    ("model", "model:delete", "删除", 4),
]

# 将按钮元组展开为与 SEED_MENUS 相同结构的 dict，合并到列表末尾
for _parent, _auth_mark, _title, _sort in _SEED_BUTTONS:
    SEED_MENUS.append({
        "parent_auth_mark": _parent, "name": "", "type": 2, "path": "",
        "auth_mark": _auth_mark, "meta": {"title": _title},
        "sort": _sort, "component": "",
    })

SEED_ROLES = [
    {"name": "超级管理员", "code": "R_ADMIN", "description": "超级管理员", "enabled": True},
]


async def seed_menus() -> dict[str, Menu]:
    """
    创建菜单，返回 {auth_mark: Menu} 映射。
    以 auth_mark 判断幂等，已存在则跳过。
    预加载全量菜单避免 N+1 查询。
    """
    # 预加载：一次性查出所有已存在的菜单
    existing = await Menu.all()
    menu_map: dict[str, Menu] = {m.auth_mark: m for m in existing if m.auth_mark}

    for item in SEED_MENUS:
        auth_mark: str = item["auth_mark"]
        if auth_mark in menu_map:
            continue

        # 解析父级 ID（优先从已创建的 menu_map 查找）
        parent_id = 0
        if parent_auth_mark := item.get("parent_auth_mark"):
            parent = menu_map.get(parent_auth_mark)
            if parent:
                parent_id = parent.id

        menu = await Menu.create(
            parent_id=parent_id,
            name=item["name"],
            type=item.get("type", 1),
            path=item["path"],
            auth_mark=auth_mark,
            meta=item["meta"],
            sort=item["sort"],
            status=True,
            component=item["component"],
        )
        menu_map[auth_mark] = menu
        app_logger.info(f"  创建菜单: {auth_mark} (id={menu.id})")

    return menu_map


async def seed_roles(menu_map: dict[str, Menu]):
    """
    创建角色并分配全部菜单权限。
    以 code 判断幂等；仅在角色首次创建时关联菜单。
    """
    all_menus = list(menu_map.values())

    for item in SEED_ROLES:
        role, created = await Role.get_or_create(
            code=item["code"],
            defaults={
                "name": item["name"],
                "description": item["description"],
                "enabled": item["enabled"],
            },
        )
        if created:
            app_logger.info(f"  创建角色: {item['code']} (id={role.id})")
            # 仅首次创建时关联菜单，后续手动配置不会被覆盖
            if all_menus:
                await role.menus.add(*all_menus)
                app_logger.info(f"  已为角色 {item['code']} 关联 {len(all_menus)} 个菜单")


async def run_seed():
    app_logger.info("开始数据初始化（seed）")

    await Tortoise.init(config=db_config)
    try:
        app_logger.info("[1/2] 初始化菜单...")
        menu_map = await seed_menus()
        app_logger.info(f"  菜单完成，共 {len(menu_map)} 条")

        app_logger.info("[2/2] 初始化角色...")
        await seed_roles(menu_map)
        app_logger.info("  角色完成")

        app_logger.info("数据初始化完成")
    finally:
        await Tortoise.close_connections()


if __name__ == "__main__":
    asyncio.run(run_seed())
