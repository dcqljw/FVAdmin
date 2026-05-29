/**
 * 操作日志工具函数
 */

/** Element Plus 标签类型 */
export type TagType = 'success' | 'primary' | 'warning' | 'danger' | 'info'

/**
 * 获取状态码对应的标签颜色
 */
export const getStatusTagType = (statusCode: number): TagType => {
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
export const getMethodTagType = (method: string): TagType => {
  return (METHOD_TAG_MAP[method] || 'info') as TagType
}

const OPERATION_TAG_MAP: Record<string, string> = {
  新增: 'success',
  删除: 'danger',
  修改: 'warning',
  查询: 'info',
  登录: 'primary',
  登出: 'info',
  导入: 'warning',
  导出: 'primary'
}

/**
 * 获取操作类型对应的标签颜色
 */
export const getOperationTagType = (operation: string): TagType => {
  return (OPERATION_TAG_MAP[operation] || 'info') as TagType
}

/**
 * 格式化 JSON 字符串，解析失败则返回原文，null 返回空字符串
 */
export const formatJson = (str: string | null): string => {
  if (!str) return ''
  try {
    return JSON.stringify(JSON.parse(str), null, 2)
  } catch {
    return str
  }
}
