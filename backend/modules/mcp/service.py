from typing import List, Optional, Tuple

from shared.base_service import BaseService
from shared.log_config import api_logger
from modules.mcp.models import McpServer, McpServerResponse
from modules.mcp.repository import mcp_server_repo
from modules.mcp import mcp_client


class McpServerService(BaseService):

    async def _get_server(self, server_id: int) -> McpServer:
        """获取服务器，不存在则抛异常"""
        server = await mcp_server_repo.get_by_id(server_id)
        if not server:
            self._not_found("MCP 服务器", str(server_id))
        return server

    async def list_servers(
            self,
            current: int = 1,
            size: int = 10,
            name: Optional[str] = None,
            code: Optional[str] = None,
            transport: Optional[str] = None,
            status: Optional[int] = None,
    ) -> Tuple[List[dict], int]:
        servers, total = await mcp_server_repo.list_paginated(
            current=current, size=size,
            name=name, code=code, transport=transport, status=status,
        )
        records = [
            McpServerResponse.model_validate(s).model_dump(mode="json")
            for s in servers
        ]
        return records, total

    async def get_all_servers(self) -> List[dict]:
        """返回全部启用的服务器（下拉选项用）"""
        servers = await mcp_server_repo.find_all_enabled()
        return [
            {"id": s.id, "name": s.name, "code": s.code, "transport": s.transport}
            for s in servers
        ]

    async def create_server(
            self,
            name: str,
            code: str,
            transport: str,
            url: str,
            auth_token: Optional[str] = None,
            description: Optional[str] = None,
            status: int = 1,
    ) -> McpServer:
        existing = await mcp_server_repo.find_by_code(code)
        if existing:
            self._already_exists("MCP 服务器", code)

        server = await mcp_server_repo.create(
            name=name,
            code=code,
            transport=transport,
            url=url,
            auth_token=auth_token or "",
            description=description or "",
            status=status,
        )
        api_logger.info(f"成功创建 MCP 服务器: {name} ({code})")
        return server

    async def update_server(
            self,
            server_id: int,
            name: str,
            transport: str,
            url: str,
            auth_token: Optional[str] = None,
            description: Optional[str] = None,
            status: Optional[int] = None,
    ) -> McpServer:
        server = await self._get_server(server_id)

        server.name = name
        server.transport = transport
        server.url = url
        # auth_token 为 None 表示不修改，空字符串表示清空
        if auth_token is not None:
            server.auth_token = auth_token
        server.description = description or ""
        if status is not None:
            server.status = status
        await server.save()

        api_logger.info(f"成功更新 MCP 服务器: {server.name} ({server.code})")
        return server

    async def delete_server(self, server_id: int) -> str:
        server = await self._get_server(server_id)

        deleted_name = server.name
        await server.delete()
        api_logger.info(f"成功删除 MCP 服务器: {deleted_name} ({server.code})")
        return deleted_name

    async def test_connection(self, server_id: int) -> dict:
        server = await self._get_server(server_id)
        return await mcp_client.test_connection(server)

    async def list_tools(self, server_id: int) -> list[dict]:
        server = await self._get_server(server_id)
        return await mcp_client.list_tools(server)

    async def list_resources(self, server_id: int) -> list[dict]:
        server = await self._get_server(server_id)
        return await mcp_client.list_resources(server)

    async def call_tool(self, server_id: int, tool_name: str, arguments: dict | None = None) -> dict:
        server = await self._get_server(server_id)
        if server.status != 1:
            from core.exceptions import CustomException
            raise CustomException(code=400, msg=f"MCP 服务器 [{server.name}] 已禁用")
        return await mcp_client.call_tool(server, tool_name, arguments)


mcp_server_service = McpServerService()
