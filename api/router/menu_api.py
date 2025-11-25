from fastapi import APIRouter, Depends

from router.deps import verify_token_dep
from schemas.response import SuccessResponse

router = APIRouter(prefix="/menu", tags=["菜单管理"])


@router.get("/menu_list")
async def menu_list():
    return SuccessResponse(data=[])


@router.post("/add_menu")
async def add_menu(uid: str = Depends(verify_token_dep)):

    return SuccessResponse(data={"message": "添加菜单成功"})
