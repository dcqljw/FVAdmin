/**
 * 操作日志工具函数
 */

/**
 * 获取状态码对应的标签颜色
 */
export const getStatusTagType = (
  statusCode: number
): 'success' | 'warning' | 'danger' | 'info' => {
  if (statusCode >= 200 && statusCode < 300) return 'success'
  if (statusCode >= 400 && statusCode < 500) return 'warning'
  if (statusCode >= 500) return 'danger'
  return 'info'
}

const METHOD_TAG_MAP: Record<string, string> = {
  GET: 'success',
  POST: 'primary',
  PUT: 'warning',
  DELETE: 'danger',
  PATCH: 'info'
}

/**
 * 获取请求方法对应的标签颜色
 */
export const getMethodTagType = (method: string) => {
  return (METHOD_TAG_MAP[method] || 'info') as
    | 'success'
    | 'primary'
    | 'warning'
    | 'danger'
    | 'info'
}
