from datetime import datetime
from typing import Optional

from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model
from pydantic import field_serializer


# ========== McpServer ==========

class McpServer(Model):
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=255, description="服务器名称")
    code = fields.CharField(max_length=100, unique=True, description="唯一标识")
    transport = fields.CharField(max_length=20, description="传输方式: sse / streamable_http")
    url = fields.CharField(max_length=1024, description="连接 URL")
    auth_token = fields.CharField(max_length=1024, default="", description="Bearer Token（可选）")
    description = fields.TextField(default="", description="描述")
    status = fields.IntField(default=1, description="状态 1启用 0禁用")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    updated_at = fields.DatetimeField(auto_now=True, description="更新时间")

    class Meta:
        table = "mcp_server"


McpServerPydantic = pydantic_model_creator(McpServer, name="McpServer")


class McpServerResponse(McpServerPydantic):
    @field_serializer("created_at", "updated_at")
    def serialize_datetime(self, value: Optional[datetime], _info):
        if value is None:
            return None
        return value.strftime("%Y-%m-%d %H:%M:%S")

    @field_serializer("auth_token")
    def mask_auth_token(self, value: str, _info):
        """返回时脱敏：只显示前4位"""
        if not value:
            return ""
        if len(value) <= 4:
            return "****"
        return value[:4] + "****"
