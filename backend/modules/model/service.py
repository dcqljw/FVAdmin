from typing import List, Tuple

from shared.base_service import BaseService
from shared.log_config import api_logger
from modules.model.models import LLMModel, LLMModelResponse
from modules.model.repository import llm_model_repo


class LLMModelService(BaseService):

    async def _get_model(self, model_id: int) -> LLMModel:
        model = await llm_model_repo.get_by_id(model_id)
        if not model:
            self._not_found("模型", str(model_id))
        return model

    async def list_models(
            self, current: int = 1, size: int = 10,
            name: str | None = None, status: int | None = None,
    ) -> Tuple[List[dict], int]:
        items, total = await llm_model_repo.list_paginated(
            current=current, size=size, name=name, status=status,
        )
        records = [
            LLMModelResponse.model_validate(m).model_dump(mode="json")
            for m in items
        ]
        return records, total

    async def create_model(self, **kwargs) -> LLMModel:
        existing = await llm_model_repo.find_by_code(kwargs["code"])
        if existing:
            self._already_exists("模型", kwargs["code"])

        if kwargs.get("is_default"):
            await self._clear_default()

        model = await llm_model_repo.create(**kwargs)
        api_logger.info(f"成功创建模型: {model.name} ({model.code})")
        return model

    async def update_model(self, model_id: int, **kwargs) -> LLMModel:
        model = await self._get_model(model_id)

        if kwargs.get("is_default"):
            await self._clear_default(exclude_id=model_id)

        for key, value in kwargs.items():
            if key == "api_key" and value is None:
                continue
            setattr(model, key, value)
        await model.save()
        api_logger.info(f"成功更新模型: {model.name} ({model.code})")
        return model

    async def delete_model(self, model_id: int) -> str:
        model = await self._get_model(model_id)
        name = model.name
        await model.delete()
        api_logger.info(f"成功删除模型: {name} ({model.code})")
        return name

    async def _clear_default(self, exclude_id: int = 0):
        await LLMModel.filter(is_default=True).exclude(id=exclude_id).update(is_default=False)


llm_model_service = LLMModelService()