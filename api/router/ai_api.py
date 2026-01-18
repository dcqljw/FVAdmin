from fastapi import APIRouter

from schemas.ai import ApiKeyCreateSchema
from models.ai_model import ApiKey
from schemas.response import ErrorResponse, SuccessResponse

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/add")
async def add_key(api_key: ApiKeyCreateSchema):
    data = await ApiKey.get_or_none(name=api_key.name)
    if data is None:
        await ApiKey.create(**api_key.model_dump())
        return SuccessResponse(message="成功")
    else:
        return ErrorResponse(message="模型已经存在")
