from datetime import datetime
from typing import Optional

from tortoise import fields
from tortoise.models import Model
from pydantic import BaseModel, field_serializer


class OperationLog(Model):
    id = fields.IntField(primary_key=True)
    user_id = fields.CharField(max_length=255, null=True, description="操作用户ID")
    username = fields.CharField(max_length=255, null=True, description="操作用户名")
    module = fields.CharField(max_length=100, description="操作模块")
    operation = fields.CharField(max_length=20, description="操作类型")
    method = fields.CharField(max_length=10, description="HTTP方法")
    path = fields.CharField(max_length=500, description="请求路径")
    query_params = fields.TextField(null=True, description="查询参数")
    request_body = fields.TextField(null=True, description="请求体")
    ip = fields.CharField(max_length=50, description="客户端IP")
    status_code = fields.IntField(description="响应状态码")
    response_body = fields.TextField(null=True, description="响应体")
    cost_time = fields.FloatField(description="请求耗时(秒)")
    created_at = fields.DatetimeField(auto_now_add=True, description="操作时间")

    class Meta:
        table = "operation_log"


class OperationLogResponse(BaseModel):
    id: int
    user_id: Optional[str] = None
    username: Optional[str] = None
    module: str
    operation: str
    method: str
    path: str
    query_params: Optional[str] = None
    request_body: Optional[str] = None
    ip: str
    status_code: int
    response_body: Optional[str] = None
    cost_time: float
    created_at: Optional[str] = None

    class Config:
        from_attributes = True

    @field_serializer("created_at")
    def serialize_datetime(self, value, _info):
        if value is None:
            return None
        if isinstance(value, datetime):
            return value.strftime("%Y-%m-%d %H:%M:%S")
        return value
