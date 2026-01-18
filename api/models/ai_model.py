from tortoise import fields
from tortoise.models import Model


class ApiKey(Model):
    name = fields.CharField(max_length=100)
    key = fields.CharField(max_length=100)
