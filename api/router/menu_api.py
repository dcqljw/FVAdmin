from fastapi import APIRouter, Depends

from core.util import convert_menu_to_tree
from models.role_model import Role, RolePydanticList
from models.user_model import User
from router.deps import verify_token_dep
from schemas.response import SuccessResponse
from schemas.menu import MenuCreateSchema
from models.menu_model import Menu, MenuPydantic, MenuPydanticList

router = APIRouter(prefix="/menu", tags=["菜单管理"])


@router.get("/list")
async def menu_list(uid: str = Depends(verify_token_dep)):
    menu_orm = await Menu.all()
    pydantic_list = MenuPydanticList(menu_orm).model_dump(mode='json')
    print(pydantic_list)
    tree = convert_menu_to_tree(pydantic_list)
    print(tree)
    return SuccessResponse(data=tree)


@router.get("/get_checked")
async def get_checked(role_id: int, uid: str = Depends(verify_token_dep)):
    related = await Role.get(id=role_id).prefetch_related("menus")
    print(related.menus.all())
    menu_name_list = [i["name"] for i in MenuPydanticList(await related.menus.all()).model_dump()]

    return SuccessResponse(data=menu_name_list)


@router.post("/add_menu")
async def add_menu(menu: MenuCreateSchema, uid: str = Depends(verify_token_dep)):
    menu = await Menu.create(**menu.model_dump())
    return SuccessResponse(data={"message": "添加菜单成功"})


@router.post("/add_permission")
async def add_permission(permission: dict):
    return {"message": "添加权限成功"}
