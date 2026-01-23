from datetime import datetime, date
from typing import List, Optional

from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator
from tortoise.models import Model
from pydantic import ConfigDict, BaseModel, field_serializer


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


class UserPydanticList(BaseModel):
    root: List[UserResponse]
