from fastapi import APIRouter, Security

from core.deps import permission_check
from shared.base_schema import SuccessResponse
from modules.system.models import User
from modules.mcp.schemas import McpServerCreateSchema, McpServerEditSchema, McpCallToolSchema
from modules.mcp.service import mcp_server_service

mcp_router = APIRouter(prefix="/mcp", tags=["MCP 服务器"])


# ========== 列表 ==========

@mcp_router.get("")
async def get_mcp_server_list(
        current: int = 1,
        size: int = 10,
        name: str | None = None,
        code: str | None = None,
        transport: str | None = None,
        status: int | None = None,
        current_user: User = Security(permission_check, scopes=["ai:mcp:list"]),
):
    records, total = await mcp_server_service.list_servers(
        current=current, size=size,
        name=name, code=code, transport=transport, status=status,
    )
    return SuccessResponse(data={"records": records, "total": total})


@mcp_router.get("/all")
async def get_all_mcp_servers(
        current_user: User = Security(permission_check, scopes=["ai:mcp:list"]),
):
    servers = await mcp_server_service.get_all_servers()
    return SuccessResponse(data=servers)


# ========== 增删改 ==========

@mcp_router.post("/add")
async def add_mcp_server(
        server: McpServerCreateSchema,
        current_user: User = Security(permission_check, scopes=["ai:mcp:add"]),
):
    result = await mcp_server_service.create_server(
        name=server.name,
        code=server.code,
        transport=server.transport,
        url=server.url,
        auth_token=server.auth_token,
        description=server.description,
        status=server.status,
    )
    return SuccessResponse(data={"id": result.id, "message": "添加成功"})


@mcp_router.post("/edit")
async def edit_mcp_server(
        server: McpServerEditSchema,
        current_user: User = Security(permission_check, scopes=["ai:mcp:edit"]),
):
    await mcp_server_service.update_server(
        server_id=server.id,
        name=server.name,
        transport=server.transport,
        url=server.url,
        auth_token=server.auth_token,
        description=server.description,
        status=server.status,
    )
    return SuccessResponse(data={"message": "修改成功"})


@mcp_router.post("/delete")
async def delete_mcp_server(
        server_id: int,
        current_user: User = Security(permission_check, scopes=["ai:mcp:delete"]),
):
    name = await mcp_server_service.delete_server(server_id)
    return SuccessResponse(data={"message": f"删除成功: {name}"})


# ========== 操作 ==========

@mcp_router.post("/test")
async def test_mcp_connection(
        server_id: int,
        current_user: User = Security(permission_check, scopes=["ai:mcp:list"]),
):
    result = await mcp_server_service.test_connection(server_id)
    return SuccessResponse(data=result)


@mcp_router.get("/{server_id}/tools")
async def get_mcp_server_tools(
        server_id: int,
        current_user: User = Security(permission_check, scopes=["ai:mcp:list"]),
):
    tools = await mcp_server_service.list_tools(server_id)
    return SuccessResponse(data=tools)


@mcp_router.get("/{server_id}/resources")
async def get_mcp_server_resources(
        server_id: int,
        current_user: User = Security(permission_check, scopes=["ai:mcp:list"]),
):
    resources = await mcp_server_service.list_resources(server_id)
    return SuccessResponse(data=resources)


@mcp_router.post("/call-tool")
async def call_mcp_tool(
        body: McpCallToolSchema,
        current_user: User = Security(permission_check, scopes=["ai:mcp:list"]),
):
    result = await mcp_server_service.call_tool(
        server_id=body.server_id,
        tool_name=body.tool_name,
        arguments=body.arguments,
    )
    return SuccessResponse(data=result)


# ========== 父路由：聚合所有子路由（供 main.py 发现） ==========

router = APIRouter(prefix="/ai")
router.include_router(mcp_router)
