from fastapi import APIRouter, Depends, Security
from tortoise.exceptions import DoesNotExist
from tortoise.functions import Count

from core.util import convert_menu_to_tree
from models.user_model import User
from models.role_model import Role
from router.deps import verify_token_dep, permission_check, get_current_user
from schemas.response import SuccessResponse, ErrorResponse
from schemas.menu import MenuCreateSchema, AddRoleMenuSchema
from models.menu_model import Menu, MenuPydanticList
from core.log_config import api_logger

router = APIRouter(prefix="/menu", tags=["菜单管理"])


@router.get("/list")
async def menu_list(current_user: User = Depends(get_current_user)):
    all_menu = []
    if current_user.username == "admin":
        all_menu.extend(await Menu.filter().all())
    else:
        data = await current_user.roles.all()
        for j in data:
            menu = await j.menus
            all_menu.extend(menu)
    # menu_orm = await Menu.all()
    pydantic_list = MenuPydanticList(all_menu).model_dump(mode='json')
    tree = convert_menu_to_tree(pydantic_list)
    return SuccessResponse(data=tree)


async def get_role_leaf_menu_ids(role_id: int):
    """
    获取角色绑定的所有叶子节点菜单ID（无下级子节点的菜单）
    优化点：批量查询子节点数量，避免循环查库
    """
    # 1. 校验角色存在性 + 预加载关联菜单（原子操作）
    try:
        role = await Role.get(id=role_id).prefetch_related("menus")
    except DoesNotExist:
        # 角色不存在时返回空列表，避免报错
        return []

    # 2. 提取选中的菜单ID（提前判空，减少后续操作）
    selected_menus = await role.menus.all()
    if not selected_menus:
        return []
    selected_menu_ids = [menu.id for menu in selected_menus]

    # 3. 批量查询所有选中菜单的子节点数量（核心优化：1次查询替代N次）
    # 查询结果格式：[{parent_id: 1, count: 0}, {parent_id: 2, count: 3}, ...]
    child_count_map = await Menu.filter(parent_id__in=selected_menu_ids) \
        .annotate(count=Count("id")) \
        .group_by("parent_id") \
        .values("parent_id", "count")

    # 4. 转换为字典，方便快速查找（O(1) 查找效率）
    count_dict = {item["parent_id"]: item["count"] for item in child_count_map}

    # 5. 筛选叶子节点（子节点数量为0的菜单ID）
    leaf_menu_ids = [
        menu_id for menu_id in selected_menu_ids
        if count_dict.get(menu_id, 0) == 0  # 无记录则默认子节点数为0
    ]

    return leaf_menu_ids


@router.get("/get_checked")
async def get_checked(role_id: int, uid: str = Depends(verify_token_dep)):
    """
    根据角色id获取对应的权限
    :param role_id:
    :param uid:
    :return:
    """
    # related = await Role.get(id=role_id).prefetch_related("menus")
    # print(related.menus.all())
    # menu_name_list = [i["name"] for i in MenuPydanticList(await related.menus.all()).model_dump()]
    leaf_menu_ids = await get_role_leaf_menu_ids(role_id)
    return SuccessResponse(data=leaf_menu_ids)


@router.post("/add")
async def add_menu(menu: MenuCreateSchema, current_user: User = Security(permission_check, scopes=['menu:add'])):
    api_logger.info(f"用户 {current_user.username} 尝试添加菜单 {menu.name}")
    await Menu.create(**menu.model_dump())
    api_logger.info(f"用户 {current_user.username} 成功添加菜单 {menu.name}")
    return SuccessResponse(data={"message": "添加菜单成功"})


@router.post("/edit")
async def edit_menu(menu_in: MenuCreateSchema, current_user: User = Security(permission_check, scopes=['menu:edit'])):
    api_logger.info(f"用户 {current_user.username} 尝试编辑菜单 {menu_in.name}")
    menu = await Menu.get_or_none(name=menu_in.name)
    if menu:
        if menu.type == 1:
            menu.name = menu_in.name
            menu.path = menu_in.path
            menu.meta = menu_in.meta
            menu.component = menu_in.component
            menu.sort = menu_in.sort
            menu.status = menu_in.status
            await menu.save()
        else:
            menu.name = menu_in.name
            menu.meta = menu_in.meta
            menu.auth_mark = menu_in.auth_mark
            await menu.save()
        api_logger.info(f"用户 {current_user.username} 成功编辑菜单 {menu_in.name}")
        return SuccessResponse(data={"message": "修改菜单成功"})
    else:
        api_logger.warning(f"编辑菜单失败：菜单 {menu_in.name} 不存在")
        return ErrorResponse(message="菜单不存在")


@router.post("/add_menu_permission")
async def add_menu_permission(role_menu: AddRoleMenuSchema):
    """
    角色添加菜单权限
    :return:
    """
    api_logger.info(f"为角色ID {role_menu.role_id} 添加菜单权限，菜单IDs: {role_menu.menu_ids}")
    data = await Role.get(id=role_menu.role_id)
    await data.menus.clear()
    menu_filter = await Menu.filter(id__in=role_menu.menu_ids)
    await data.menus.add(*menu_filter)
    # Role.menus.add()
    api_logger.info(f"角色ID {role_menu.role_id} 菜单权限添加成功")
    return SuccessResponse(data={"message": "添加菜单成功"})


@router.post("/delete")
async def delete_menu(menu_id: int,
                      current_user: User = Security(permission_check, scopes=['menu:delete'])):
    api_logger.info(f"用户 {current_user.username} 尝试删除菜单ID {menu_id}")
    menu = await Menu.get_or_none(id=menu_id)
    if menu.name == "Menus":
        api_logger.warning(f"用户 {current_user.username} 尝试删除根菜单，操作被拒绝")
        return ErrorResponse(message="不能删除根菜单")
    else:
        await Menu.filter(parent_id=menu_id).delete()
        await menu.delete()
        api_logger.info(f"用户 {current_user.username} 成功删除菜单 {menu.name}")
        return SuccessResponse(data={"message": "删除菜单成功"})
