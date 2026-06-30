from typing import Optional, List, Tuple

from shared.base_repository import BaseRepository
from modules.model.models import LLMModel


class LLMModelRepository(BaseRepository[LLMModel]):
    model_class = LLMModel

    async def find_by_code(self, code: str) -> Optional[LLMModel]:
        return await self.get_or_none(code=code)

    async def get_default(self) -> Optional[LLMModel]:
        return await self.get_or_none(is_default=True, status=1)

    async def list_paginated(
            self,
            current: int = 1,
            size: int = 10,
            name: Optional[str] = None,
            status: Optional[int] = None,
    ) -> Tuple[List[LLMModel], int]:
        query = LLMModel.all()
        if name:
            query = query.filter(name__contains=name)
        if status is not None:
            query = query.filter(status=status)

        total = await query.count()
        items = await query.order_by("-is_default", "-id").offset((current - 1) * size).limit(size).all()
        return list(items), total


llm_model_repo = LLMModelRepository(LLMModel)