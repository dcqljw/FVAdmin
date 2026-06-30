from datetime import datetime
from typing import Optional

from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model
from pydantic import field_serializer


# ========== ChatSession ==========

class ChatSession(Model):
    """对话会话"""
    id = fields.IntField(primary_key=True)
    user = fields.ForeignKeyField(
        "models.User", related_name="chat_sessions", on_delete=fields.CASCADE,
    )
    title = fields.CharField(max_length=255, default="新对话", description="会话标题")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    updated_at = fields.DatetimeField(auto_now=True, description="更新时间")

    class Meta:
        table = "chat_session"


ChatSessionPydantic = pydantic_model_creator(ChatSession, name="ChatSession")


class ChatSessionResponse(ChatSessionPydantic):
    @field_serializer("created_at", "updated_at")
    def serialize_datetime(self, value: Optional[datetime], _info):
        if value is None:
            return None
        return value.strftime("%Y-%m-%d %H:%M:%S")


# ========== ChatMessage ==========

class ChatMessage(Model):
    """对话消息"""
    id = fields.IntField(primary_key=True)
    session = fields.ForeignKeyField(
        "models.ChatSession", related_name="messages", on_delete=fields.CASCADE,
    )
    role = fields.CharField(max_length=20, description="角色: system / user / assistant / tool")
    content = fields.TextField(description="消息内容")
    tool_calls = fields.TextField(default="", description="工具调用 JSON（assistant 消息）")
    tool_call_id = fields.CharField(max_length=100, default="", description="工具调用 ID（tool 消息）")
    tool_name = fields.CharField(max_length=100, default="", description="工具名称（tool 消息）")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")

    class Meta:
        table = "chat_message"


ChatMessagePydantic = pydantic_model_creator(ChatMessage, name="ChatMessage")


class ChatMessageResponse(ChatMessagePydantic):
    @field_serializer("created_at")
    def serialize_datetime(self, value: Optional[datetime], _info):
        if value is None:
            return None
        return value.strftime("%Y-%m-%d %H:%M:%S")