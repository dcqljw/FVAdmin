from datetime import datetime
from typing import Optional

from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator
from tortoise.models import Model
from pydantic import field_serializer


# ========== User ==========

class User(Model):
    id = fields.IntField(primary_key=True)
    username = fields.CharField(max_length=255, unique=True, description="用户名")
    nickname = fields.CharField(max_length=255, description="昵称")
    password = fields.CharField(max_length=255, description="密码")
    email = fields.CharField(max_length=255, description="邮箱")
    phone = fields.CharField(max_length=11, description="手机号")
    avatar = fields.CharField(default="", max_length=255, description="头像")
    status = fields.IntField(default=1, description="状态")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    updated_at = fields.DatetimeField(auto_now=True, description="更新时间")

    roles = fields.ManyToManyField("models.Role", related_name="users")

    class Meta:
        indexes = [
            ("username",),
        ]


UserPydantic = pydantic_model_creator(
    User,
    name="User",
    exclude=("password",)
)


class UserResponse(UserPydantic):
    # 使用 field_serializer 处理 datetime 字段
    @field_serializer("created_at", "updated_at")
    def serialize_datetime(self, value: Optional[datetime], _info):
        if value is None:
            return None
        return value.strftime("%Y-%m-%d %H:%M:%S")


# ========== Role ==========

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


class RoleResponse(RolePydantic):
    # 使用 field_serializer 处理 datetime 字段
    @field_serializer("created_at", "updated_at")
    def serialize_datetime(self, value: Optional[datetime], _info):
        if value is None:
            return None
        return value.strftime("%Y-%m-%d %H:%M:%S")


# ========== Menu ==========

class Menu(Model):
    id = fields.IntField(primary_key=True)
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
)
MenuPydanticList = pydantic_queryset_creator(Menu, name="MenuList")
