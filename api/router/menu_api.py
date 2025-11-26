from fastapi import APIRouter, Depends

from router.deps import verify_token_dep
from schemas.response import SuccessResponse
from schemas.menu import MenuCreateSchema
from models.menu_model import Menu, MenuPydantic

router = APIRouter(prefix="/menu", tags=["菜单管理"])


@router.get("/menu_list")
async def menu_list():
    menu = await Menu.filter().all()
    for m in menu:
        data = await MenuPydantic.from_tortoise_orm(m)
        data = data.model_dump()
        print(data)
    return menu


@router.post("/add_menu")
async def add_menu(menu: MenuCreateSchema, uid: str = Depends(verify_token_dep)):
    menu = await Menu.create(**menu.model_dump())
    return SuccessResponse(data={"message": "添加菜单成功"})
