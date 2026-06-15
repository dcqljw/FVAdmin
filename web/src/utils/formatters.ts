/**
 * 通用格式化工具函数
 *
 * 提供表格列格式化等共用函数，避免在多个组件中重复实现
 */

import { h } from 'vue'
import { ElTag } from 'element-plus'

/** 用户启用状态值 */
export const USER_STATUS = {
  DISABLED: 0,
  ENABLED: 1
} as const

/**
 * 格式化用户启用/禁用状态为标签
 *
 * @param status 状态值（0: 禁用, 1: 启用）
 * @returns VNode 标签组件
 */
export const formatUserStatusTag = (status: number) => {
  const config =
    status === USER_STATUS.ENABLED
      ? { type: 'success' as const, text: '启用' }
      : { type: 'danger' as const, text: '禁用' }
  return h(ElTag, { type: config.type }, () => config.text)
}
