from fastapi import APIRouter, Depends

from core.util import convert_menu_to_tree
from models.role_model import Role, RolePydanticList
from models.user_model import User
from router.deps import verify_token_dep
from schemas.response import SuccessResponse
from schemas.menu import MenuCreateSchema, AddRoleMenuSchema
from models.menu_model import Menu, MenuPydantic, MenuPydanticList

router = APIRouter(prefix="/menu", tags=["菜单管理"])


@router.get("/list")
async def menu_list(uid: str = Depends(verify_token_dep)):
    """
    根据用户权限获取菜单列表
    :param uid:
    :return:
    """
    data = await User.get(id=uid).prefetch_related("roles")
    all_menu = []
    for j in data.roles:
        menu = await j.menus
        all_menu.extend(menu)
    # menu_orm = await Menu.all()
    pydantic_list = MenuPydanticList(all_menu).model_dump(mode='json')
    tree = convert_menu_to_tree(pydantic_list)
    return SuccessResponse(data=tree)


@router.get("/get_checked")
async def get_checked(role_id: int, uid: str = Depends(verify_token_dep)):
    """
    根据角色id获取对应的权限
    :param role_id:
    :param uid:
    :return:
    """
    related = await Role.get(id=role_id).prefetch_related("menus")
    print(related.menus.all())
    menu_name_list = [i["name"] for i in MenuPydanticList(await related.menus.all()).model_dump()]
    return SuccessResponse(data=menu_name_list)


@router.post("/add_menu_permission")
async def add_menu_permission(role_menu: AddRoleMenuSchema):
    """
    角色添加菜单权限
    :return:
    """
    print(*role_menu.menu_ids)
    data = await Role.get(id=role_menu.role_id)
    await data.menus.clear()
    menu_filter = await Menu.filter(id__in=role_menu.menu_ids)
    await data.menus.add(*menu_filter)
    # Role.menus.add()
    return SuccessResponse(data={"message": "添加菜单成功"})


@router.post("/add_menu")
async def add_menu(menu: MenuCreateSchema, uid: str = Depends(verify_token_dep)):
    menu = await Menu.create(**menu.model_dump())
    return SuccessResponse(data={"message": "添加菜单成功"})


@router.post("/add_permission")
async def add_permission(permission: dict):
    return {"message": "添加权限成功"}
