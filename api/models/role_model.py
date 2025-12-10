from datetime import datetime

from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator
from pydantic import ConfigDict


class Role(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(unique=True, max_length=255)
    code = fields.CharField(unique=True, max_length=255)
    description = fields.CharField(max_length=255)
    enabled = fields.IntField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    menus = fields.ManyToManyField("models.Menu", related_name="menus")


RolePydantic = pydantic_model_creator(
    Role,
    name="Role",
    model_config=ConfigDict(
        json_encoders={datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S") if v else None}
    )
)
RolePydanticList = pydantic_queryset_creator(Role, name="RoleList")
