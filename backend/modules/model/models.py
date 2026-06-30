from datetime import datetime
from typing import Optional

from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model
from pydantic import field_serializer


class LLMModel(Model):
    """大语言模型配置"""
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=255, description="模型名称")
    code = fields.CharField(max_length=100, unique=True, description="唯一标识")
    provider = fields.CharField(max_length=100, default="", description="提供商")
    base_url = fields.CharField(max_length=1024, description="API Base URL")
    api_key = fields.CharField(max_length=1024, description="API Key")
    model_name = fields.CharField(max_length=100, description="模型标识（如 gpt-4o, deepseek-chat）")
    max_tokens = fields.IntField(default=2048, description="最大输出 token 数")
    is_default = fields.BooleanField(default=False, description="是否默认模型")
    status = fields.IntField(default=1, description="状态 1启用 0禁用")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    updated_at = fields.DatetimeField(auto_now=True, description="更新时间")

    class Meta:
        table = "llm_model"


LLMModelPydantic = pydantic_model_creator(LLMModel, name="LLMModel")


class LLMModelResponse(LLMModelPydantic):
    @field_serializer("created_at", "updated_at")
    def serialize_datetime(self, value: Optional[datetime], _info):
        if value is None:
            return None
        return value.strftime("%Y-%m-%d %H:%M:%S")
