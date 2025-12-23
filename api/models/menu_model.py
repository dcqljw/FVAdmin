from datetime import datetime

from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator
from pydantic import ConfigDict


class Menu(Model):
    id = fields.IntField(pk=True)
    parent_id = fields.IntField(default=0, description="父级id")
    name = fields.CharField(max_length=255, description="菜单名称|按钮名称")
    type = fields.IntField(default=1, description="类型 1菜单2按钮")
    path = fields.CharField(max_length=255, description="菜单路径")
    auth_mark = fields.CharField(max_length=255, description="按钮权限标识")
    meta = fields.JSONField(description="菜单元数据", null=True)
    sort = fields.IntField(default=0, description="排序")
    status = fields.BooleanField(default=True, description="状态")
    component = fields.CharField(max_length=255, description="页面路径")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    updated_at = fields.DatetimeField(auto_now=True, description="更新时间")

    class PydanticMeta:
        exclude = ["created_at", "updated_at"]


MenuPydantic = pydantic_model_creator(
    Menu,
    name="Menu",
    model_config=ConfigDict(
        json_encoders={datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")}
    )
)
MenuPydanticList = pydantic_queryset_creator(Menu, name="MenuList")
