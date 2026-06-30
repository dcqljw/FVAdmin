"""
MCP 客户端封装

负责与外部 MCP 服务器建立连接，提供统一的调用接口。
支持 SSE 和 Streamable HTTP 两种传输方式。
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

import httpx
from mcp import ClientSession
from mcp.client.sse import sse_client
from mcp.client.streamable_http import streamable_http_client
from mcp.types import (
    TextContent,
    ImageContent,
    EmbeddedResource,
    BlobResourceContents,
)

from modules.mcp.models import McpServer
from shared.log_config import api_logger


@asynccontextmanager
async def mcp_session(server: McpServer) -> AsyncGenerator[ClientSession, None]:
    """
    创建一个 MCP 会话上下文。

    用法：
        async with mcp_session(server) as session:
            tools = await session.list_tools()
            result = await session.call_tool("tool_name", {"arg": "value"})
    """
    headers = {}
    if server.auth_token:
        headers["Authorization"] = f"Bearer {server.auth_token}"

    api_logger.debug(f"连接 MCP 服务器: {server.code} ({server.transport}) -> {server.url}")

    if server.transport == "sse":
        async with sse_client(server.url, headers=headers if headers else None) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                yield session

    elif server.transport == "streamable_http":
        http_client = httpx.AsyncClient(headers=headers) if headers else None
        async with streamable_http_client(server.url, http_client=http_client) as (read, write, _):
            async with ClientSession(read, write) as session:
                await session.initialize()
                yield session

    else:
        raise ValueError(f"不支持的传输方式: {server.transport}")


async def list_tools(server: McpServer) -> list[dict]:
    """列出指定 MCP 服务器的所有工具"""
    async with mcp_session(server) as session:
        result = await session.list_tools()
        return [
            {
                "name": tool.name,
                "description": tool.description or "",
                "inputSchema": tool.inputSchema,
            }
            for tool in result.tools
        ]


async def list_resources(server: McpServer) -> list[dict]:
    """列出指定 MCP 服务器的所有资源"""
    async with mcp_session(server) as session:
        result = await session.list_resources()
        return [
            {
                "uri": str(resource.uri),
                "name": resource.name,
                "description": resource.description or "",
                "mimeType": resource.mimeType or "",
            }
            for resource in result.resources
        ]


async def call_tool(server: McpServer, tool_name: str, arguments: dict | None = None) -> dict:
    """
    调用指定 MCP 服务器的工具。

    返回：
        {"content": [...], "isError": bool}
    """
    async with mcp_session(server) as session:
        result = await session.call_tool(tool_name, arguments)
        content = []
        for item in result.content:
            if isinstance(item, TextContent):
                content.append({"type": "text", "text": item.text})
            elif isinstance(item, ImageContent):
                content.append({"type": "image", "data": item.data, "mimeType": item.mimeType})
            elif isinstance(item, EmbeddedResource):
                resource = item.resource
                if isinstance(resource, BlobResourceContents):
                    content.append({"type": "blob", "blob": resource.blob, "mimeType": resource.mimeType or ""})
                else:
                    # TextResourceContents
                    content.append({"type": "text", "text": resource.text})
            else:
                content.append({"type": "unknown", "raw": str(item)})
        return {
            "content": content,
            "isError": result.isError,
        }


async def test_connection(server: McpServer) -> dict:
    """
    测试与 MCP 服务器的连接。

    返回：
        {"success": bool, "tools_count": int, "resources_count": int, "error": str | None}
    """
    try:
        async with mcp_session(server) as session:
            tools_result = await session.list_tools()
            resources_result = await session.list_resources()
            return {
                "success": True,
                "tools_count": len(tools_result.tools),
                "resources_count": len(resources_result.resources),
                "error": None,
            }
    except Exception as e:
        api_logger.warning(f"MCP 连接测试失败 [{server.code}]: {e}")
        return {
            "success": False,
            "tools_count": 0,
            "resources_count": 0,
            "error": str(e),
        }
