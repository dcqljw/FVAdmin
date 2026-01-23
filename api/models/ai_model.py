from tortoise import fields
from tortoise.models import Model


class LLMModel(Model):
    baseUrl = fields.TextField()
    name = fields.CharField(max_length=100)
    apiKey = fields.CharField(max_length=100)
