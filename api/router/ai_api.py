from fastapi import APIRouter, Security

from models.user_model import User
from router.deps import permission_check
from schemas.ai import ApiKeyCreateSchema
from models.ai_model import LLMModel, LLMModelPydanticList
from schemas.response import ErrorResponse, SuccessResponse

router = APIRouter(prefix="/ai", tags=["ai"])


@router.get("/list")
async def get_key_list(current_user: User = Security(permission_check, scopes=['ai:list'])):
    data = await LLMModel.filter().all()
    data = LLMModelPydanticList(data).model_dump(mode='json')
    return SuccessResponse(data=data)


@router.post("/add")
async def add_key(api_key: ApiKeyCreateSchema, current_user: User = Security(permission_check, scopes=['ai:add'])):
    data = await LLMModel.get_or_none(name=api_key.name)
    if data is None:
        await LLMModel.create(**api_key.model_dump())
        return SuccessResponse(message="成功")
    else:
        return ErrorResponse(message="模型已经存在")
