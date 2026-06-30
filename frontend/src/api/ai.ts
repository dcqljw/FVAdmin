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

/** 获取模型配置列表 */
export function fetchGetModelConfigList(params: Api.Ai.ModelConfigSearchParams) {
  return request.get<Api.Ai.ModelConfigList>({
    url: '/api/model',
    params
  })
}

/** 新增模型配置 */
export function fetchAddModelConfig(formData: Partial<Api.Ai.ModelConfigItem>) {
  return request.post<any>({
    url: '/api/model/add',
    data: formData
  })
}

/** 编辑模型配置 */
export function fetchUpdateModelConfig(formData: Partial<Api.Ai.ModelConfigItem>) {
  return request.post<any>({
    url: '/api/model/edit',
    data: formData
  })
}

/** 删除模型配置 */
export function fetchDeleteModelConfig(id: number) {
  return request.post<any>({
    url: `/api/model/delete?model_id=${id}`
  })
}
