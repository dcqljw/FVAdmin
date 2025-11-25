from tortoise import fields
from tortoise.models import Model


class Menu(Model):
    id = fields.IntField(pk=True)
    parent_id = fields.IntField(default=0, description="父级id")
    name = fields.CharField(max_length=255, description="菜单名称")
    path = fields.CharField(max_length=255, description="菜单路径")
    menu_type = fields.IntField(description="菜单类型")
    meta = fields.JSONField(description="菜单元数据", null=True)
    component = fields.CharField(max_length=255, description="页面路径")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    updated_at = fields.DatetimeField(auto_now=True, description="更新时间")
