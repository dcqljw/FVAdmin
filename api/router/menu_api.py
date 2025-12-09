from fastapi import APIRouter, Depends

from models.user_model import User
from router.deps import verify_token_dep
from schemas.response import SuccessResponse
from schemas.menu import MenuCreateSchema
from models.menu_model import Menu, MenuPydantic

router = APIRouter(prefix="/menu", tags=["菜单管理"])


@router.get("/menu_list")
async def menu_list(uid: str = Depends(verify_token_dep)):
    user = await User.get_or_none(id=uid).prefetch_related("roles__menus")
    menu_set = set()
    for i in user.roles:
        for j in i.menus:
            menu_set.add(j.id)

    menu = await Menu.filter(parent_id=0).all()
    result_menu_list = []
    for i in menu:
        if i.id not in menu_set:
             continue
        item = await MenuPydantic.from_tortoise_orm(i)
        item = item.model_dump(exclude={"created_at", "updated_at"})
        item["menu"] = f"/{item['path']}"
        item["children"] = []
        children_list = await Menu.filter(parent_id=i.id).all()
        for j in children_list:
            if j.id not in menu_set:
                continue
            children = await MenuPydantic.from_tortoise_orm(j)
            children = children.model_dump(exclude={"created_at", "updated_at"})
            if children["menu_type"] == 1:
                children["menu"] = f"/{item['path']}/{children['path']}"
            item["children"].append(children)
        result_menu_list.append(item)

    print(result_menu_list)

    return SuccessResponse(data=result_menu_list)


@router.post("/add_menu")
async def add_menu(menu: MenuCreateSchema, uid: str = Depends(verify_token_dep)):
    menu = await Menu.create(**menu.model_dump())
    return SuccessResponse(data={"message": "添加菜单成功"})


@router.post("/add_permission")
async def add_permission(permission: dict):
    return {"message": "添加权限成功"}
