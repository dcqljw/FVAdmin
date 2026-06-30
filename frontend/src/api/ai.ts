import request from '@/utils/http'

/** 获取 MCP Server 列表 */
export function fetchGetMcpServerList(params: Api.Ai.McpServerSearchParams) {
  return request.get<Api.Ai.McpServerList>({
    url: '/api/ai/mcp',
    params
  })
}

/** 新增 MCP Server */
export function fetchAddMcpServer(formData: Partial<Api.Ai.McpServerItem>) {
  return request.post<any>({
    url: '/api/ai/mcp/add',
    data: formData
  })
}

/** 编辑 MCP Server */
export function fetchUpdateMcpServer(formData: Partial<Api.Ai.McpServerItem>) {
  return request.post<any>({
    url: '/api/ai/mcp/edit',
    data: formData
  })
}

/** 删除 MCP Server */
export function fetchDeleteMcpServer(id: number) {
  return request.post<any>({
    url: `/api/ai/mcp/delete?mcp_id=${id}`
  })
}

/** 测试 MCP Server — 获取可用工具列表 */
export function fetchTestMcpServer(id: number) {
  return request.get<Api.Ai.McpServerTool[]>({
    url: `/api/ai/mcp/${id}/tools`
  })
}
