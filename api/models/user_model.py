from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator
from tortoise.models import Model


class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=255, unique=True, description="用户名")
    nickname = fields.CharField(max_length=255, description="昵称")
    password = fields.CharField(max_length=255, description="密码")
    email = fields.CharField(max_length=255, description="邮箱")
    phone = fields.CharField(max_length=11, description="手机号")
    avatar = fields.CharField(max_length=255, description="头像")
    status = fields.IntField(default=1, description="状态")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    updated_at = fields.DatetimeField(auto_now=True, description="更新时间")

    roles = fields.ManyToManyField("models.Role", related_name="users")


UserPydantic = pydantic_model_creator(User, name="User", exclude=("password",))
UserPydanticList = pydantic_queryset_creator(User, exclude=("password",))
