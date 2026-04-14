from fastapi import APIRouter, Depends, Security

from models.user_model import User
from router.deps import verify_token_dep, permission_check, get_current_user
from schemas.response import SuccessResponse
from schemas.menu import MenuCreateSchema, AddRoleMenuSchema
from services import menu_service

router = APIRouter(prefix="/menu", tags=["菜单管理"])


@router.get("/list")
async def menu_list(current_user: User = Depends(get_current_user)):
    tree = await menu_service.get_menu_tree_for_user(current_user)
    return SuccessResponse(data=tree)


@router.get("/get_checked")
async def get_checked(role_id: int, uid: str = Depends(verify_token_dep)):
    """
    根据角色id获取对应的权限
    :param role_id:
    :param uid:
    :return:
    """
    leaf_menu_ids = await menu_service.get_role_leaf_menu_ids(role_id)
    return SuccessResponse(data=leaf_menu_ids)


@router.post("/add")
async def add_menu(
    menu: MenuCreateSchema,
    current_user: User = Security(permission_check, scopes=['menu:add']),
):
    await menu_service.create_menu(
        parent_id=menu.parent_id, name=menu.name, path=menu.path,
        meta=menu.meta, component=menu.component, sort=menu.sort,
        status=menu.status, auth_mark=menu.auth_mark, menu_type=menu.type,
    )
    return SuccessResponse(data={"message": "添加菜单成功"})


@router.post("/edit")
async def edit_menu(
    menu_in: MenuCreateSchema,
    current_user: User = Security(permission_check, scopes=['menu:edit']),
):
    await menu_service.update_menu(
        name=menu_in.name, path=menu_in.path, meta=menu_in.meta,
        component=menu_in.component, sort=menu_in.sort,
        status=menu_in.status, auth_mark=menu_in.auth_mark, menu_type=menu_in.type,
    )
    return SuccessResponse(data={"message": "修改菜单成功"})


@router.post("/add_menu_permission")
async def add_menu_permission(role_menu: AddRoleMenuSchema):
    """
    角色添加菜单权限
    :return:
    """
    await menu_service.assign_menus_to_role(
        role_id=role_menu.role_id, menu_ids=role_menu.menu_ids,
    )
    return SuccessResponse(data={"message": "添加菜单成功"})


@router.post("/delete")
async def delete_menu(
    menu_id: int,
    current_user: User = Security(permission_check, scopes=['menu:delete']),
):
    await menu_service.delete_menu(menu_id=menu_id)
    return SuccessResponse(data={"message": "删除菜单成功"})
