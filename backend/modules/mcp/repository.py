from typing import Optional, List, Tuple

from shared.base_repository import BaseRepository
from modules.mcp.models import McpServer


class McpServerRepository(BaseRepository[McpServer]):
    model_class = McpServer

    async def find_by_code(self, code: str) -> Optional[McpServer]:
        return await self.get_or_none(code=code)

    async def list_paginated(
            self,
            current: int = 1,
            size: int = 10,
            name: Optional[str] = None,
            code: Optional[str] = None,
            transport: Optional[str] = None,
            status: Optional[int] = None,
    ) -> Tuple[List[McpServer], int]:
        query = McpServer.all()
        if name:
            query = query.filter(name__contains=name)
        if code:
            query = query.filter(code__contains=code)
        if transport:
            query = query.filter(transport=transport)
        if status is not None:
            query = query.filter(status=status)

        total = await query.count()
        servers = await query.offset((current - 1) * size).limit(size).all()
        return list(servers), total

    async def find_all_enabled(self) -> List[McpServer]:
        return await self.filter(status=1)


mcp_server_repo = McpServerRepository(McpServer)
