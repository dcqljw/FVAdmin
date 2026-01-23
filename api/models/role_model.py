from datetime import datetime
from typing import Optional, List

from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator
from pydantic import ConfigDict, field_serializer, BaseModel


class Role(Model):
    id = fields.IntField(primary_key=True)
    name = fields.CharField(unique=True, max_length=255)
    code = fields.CharField(unique=True, max_length=255)
    description = fields.CharField(max_length=255)
    enabled = fields.BooleanField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    menus = fields.ManyToManyField("models.Menu", related_name="menus")


RolePydantic = pydantic_model_creator(
    Role,
    name="Role",
)
RolePydanticList = pydantic_queryset_creator(Role, name="RoleList")


class RoleResponse(RolePydantic):
    # 使用 field_serializer 处理 datetime 字段
    @field_serializer("created_at", "updated_at")
    def serialize_datetime(self, value: Optional[datetime], _info):
        if value is None:
            return None
        return value.strftime("%Y-%m-%d %H:%M:%S")


class RoleListResponse(BaseModel):
    data: List[RoleResponse]
