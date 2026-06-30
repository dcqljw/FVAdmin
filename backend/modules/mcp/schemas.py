from typing import Any, Literal

from pydantic import BaseModel


# ========== McpServer Schemas ==========

TransportType = Literal["sse", "streamable_http"]


class McpServerCreateSchema(BaseModel):
    name: str
    code: str
    transport: TransportType
    url: str
    auth_token: str | None = None
    description: str | None = None
    status: int = 1


class McpServerEditSchema(BaseModel):
    id: int
    name: str
    transport: TransportType
    url: str
    auth_token: str | None = None
    description: str | None = None
    status: int | None = None


class McpCallToolSchema(BaseModel):
    server_id: int
    tool_name: str
    arguments: dict[str, Any] | None = None
