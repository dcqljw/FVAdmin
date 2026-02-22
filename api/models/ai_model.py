from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator


class LLMModel(Model):
    name = fields.CharField(max_length=100, default="")
    base_url = fields.TextField()
    model = fields.CharField(max_length=100, default="")
    api_key = fields.CharField(max_length=100, default="")


LLMModelPydanticList = pydantic_queryset_creator(LLMModel)
