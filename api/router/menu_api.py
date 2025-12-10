from fastapi import APIRouter, Depends

from core.util import convert_menu_to_tree
from models.user_model import User
from router.deps import verify_token_dep
from schemas.response import SuccessResponse
from schemas.menu import MenuCreateSchema
from models.menu_model import Menu, MenuPydantic, MenuPydanticList

router = APIRouter(prefix="/menu", tags=["菜单管理"])


@router.get("/list")
async def menu_list(uid: str = Depends(verify_token_dep)):
    d = [
        {
            "name": "Dashboard",
            "path": "/dashboard",
            "component": "/index/index",
            "meta": {
                "title": "menus.dashboard.title",
                "icon": "ri:pie-chart-line"
            },
            "children": [
                {
                    "path": "console",
                    "name": "Console",
                    "component": "/dashboard/console",
                    "meta": {
                        "title": "menus.dashboard.console",
                        "icon": "ri:home-smile-2-line",
                        "keepAlive": False,
                        "fixedTab": True
                    }
                },
            ]
        },
        {
            "name": "System",
            "path": "/system",
            "component": "/index/index",
            "meta": {
                "title": "menus.system.title",
                "icon": "ri:user-3-line"
            },
            "children": [
                {
                    "path": "user",
                    "name": "User",
                    "component": "/system/user",
                    "meta": {
                        "title": "menus.system.user",
                        "icon": "ri:user-line",
                        "keepAlive": True,
                    }
                },
            ]
        }
    ]
    menu_orm = await Menu.all()
    pydantic_list = MenuPydanticList(menu_orm).model_dump(mode='json')
    print(pydantic_list)
    tree = convert_menu_to_tree(pydantic_list)
    print(tree)
    return SuccessResponse(data=tree)
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
