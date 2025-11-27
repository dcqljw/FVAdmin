from tortoise import fields
from tortoise.models import Model


class Role(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(unique=True, max_length=255)
    code = fields.CharField(unique=True, max_length=255)
    description = fields.CharField(max_length=255)
    status = fields.IntField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    menus = fields.ManyToManyField("models.Menu", related_name="permissions")
