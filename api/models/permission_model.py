from tortoise import fields
from tortoise.models import Model


class Permission(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    code = fields.CharField(max_length=255)
    description = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField()

    menus = fields.ManyToManyField("models.Menu", related_name="permissions")
