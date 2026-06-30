from fastapi import APIRouter, Security

from core.deps import permission_check
from shared.base_schema import SuccessResponse
from modules.system.models import User
from modules.model.schemas import LLMModelCreateSchema, LLMModelEditSchema
from modules.model.service import llm_model_service

model_router = APIRouter(prefix="/model", tags=["模型管理"])


@model_router.get("")
async def get_model_list(
        current: int = 1,
        size: int = 10,
        name: str | None = None,
        status: int | None = None,
        current_user: User = Security(permission_check, scopes=["model:list"]),
):
    records, total = await llm_model_service.list_models(
        current=current, size=size, name=name, status=status,
    )
    return SuccessResponse(data={"records": records, "total": total})


@model_router.post("/add")
async def add_model(
        body: LLMModelCreateSchema,
        current_user: User = Security(permission_check, scopes=["model:add"]),
):
    result = await llm_model_service.create_model(**body.model_dump())
    return SuccessResponse(data={"id": result.id, "message": "添加成功"})


@model_router.post("/edit")
async def edit_model(
        body: LLMModelEditSchema,
        current_user: User = Security(permission_check, scopes=["model:edit"]),
):
    await llm_model_service.update_model(body.id, **body.model_dump(exclude={"id"}))
    return SuccessResponse(data={"message": "修改成功"})


@model_router.post("/delete")
async def delete_model(
        model_id: int,
        current_user: User = Security(permission_check, scopes=["model:delete"]),
):
    name = await llm_model_service.delete_model(model_id)
    return SuccessResponse(data={"message": f"删除成功: {name}"})


router = APIRouter()
router.include_router(model_router)