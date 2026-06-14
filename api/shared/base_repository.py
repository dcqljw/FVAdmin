from typing import Generic, TypeVar, Optional, Type, List

from tortoise.models import Model

ModelT = TypeVar("ModelT", bound=Model)


class BaseRepository(Generic[ModelT]):
    """泛型 Repository 基类，封装 Tortoise ORM 通用操作"""

    model_class: Type[ModelT]

    def __init__(self, model_class: Type[ModelT]):
        self.model_class = model_class

    async def get_by_id(self, id_val) -> Optional[ModelT]:
        return await self.model_class.get_or_none(id=id_val)

    async def get_or_none(self, **filters) -> Optional[ModelT]:
        return await self.model_class.get_or_none(**filters)

    async def create(self, **kwargs) -> ModelT:
        return await self.model_class.create(**kwargs)

    async def bulk_create(self, objs: List[ModelT]) -> None:
        await self.model_class.bulk_create(objs)

    async def filter(self, **filters):
        return await self.model_class.filter(**filters)

    async def all(self):
        return await self.model_class.all()

    async def count(self, **filters) -> int:
        return await self.model_class.filter(**filters).count()

    async def exists(self, **filters) -> bool:
        return await self.model_class.filter(**filters).exists()
