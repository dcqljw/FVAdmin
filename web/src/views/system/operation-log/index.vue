<!-- 操作日志 -->
<template>
  <div class="art-full-height">
    <ElCard class="art-table-card" shadow="never">
      <ArtTableHeader v-model:columns="columnChecks" :loading="loading" @refresh="refreshData">
        <template #left>
          <ArtExcelExport
            :data="data"
            filename="操作日志"
            sheet-name="操作日志"
            :auto-index="true"
            :columns="exportColumns"
            size="default"
          />
        </template>
      </ArtTableHeader>

      <ArtTable
        :loading="loading"
        :data="data"
        :columns="columns"
        :pagination="pagination"
        @pagination:size-change="handleSizeChange"
        @pagination:current-change="handleCurrentChange"
      />
    </ElCard>
  </div>
</template>

<script setup lang="ts">
  import { useTable } from '@/hooks/core/useTable'
  import { fetchGetOperationLogList } from '@/api/system-manage'
  import { ElTag } from 'element-plus'
  import ArtExcelExport from '@/components/core/forms/art-excel-export/index.vue'

  defineOptions({ name: 'OperationLog' })

  type OperationLogItem = Api.OperationLog.OperationLogItem

  /** Excel 导出列配置 */
  const exportColumns = {
    username: { title: '用户名' },
    module: { title: '操作模块' },
    operation: { title: '操作类型' },
    method: { title: '请求方法' },
    path: { title: '请求路径' },
    ip: { title: 'IP' },
    status_code: { title: '状态码' },
    cost_time: { title: '耗时(s)' },
    created_at: { title: '操作时间' }
  }

  /**
   * 获取状态码对应的标签颜色
   */
  const getStatusTagType = (statusCode: number): 'success' | 'warning' | 'danger' | 'info' => {
    if (statusCode >= 200 && statusCode < 300) return 'success'
    if (statusCode >= 400 && statusCode < 500) return 'warning'
    if (statusCode >= 500) return 'danger'
    return 'info'
  }

  /**
   * 获取请求方法对应的标签颜色
   */
  const getMethodTagType = (method: string) => {
    const map: Record<string, string> = {
      GET: 'success',
      POST: 'primary',
      PUT: 'warning',
      DELETE: 'danger',
      PATCH: 'info'
    }
    return (map[method] || 'info') as any
  }

  const {
    columns,
    columnChecks,
    data,
    loading,
    pagination,
    handleSizeChange,
    handleCurrentChange,
    refreshData
  } = useTable({
    core: {
      apiFn: fetchGetOperationLogList,
      apiParams: {
        current: 1,
        size: 20
      },
      columnsFactory: () => [
        { type: 'index', width: 60, label: '序号' },
        { prop: 'username', label: '用户名', width: 120 },
        { prop: 'module', label: '操作模块', width: 150 },
        {
          prop: 'operation',
          label: '操作类型',
          width: 100
        },
        {
          prop: 'method',
          label: '请求方法',
          width: 100,
          formatter: (row: OperationLogItem) => {
            return h(ElTag, { type: getMethodTagType(row.method) }, () => row.method)
          }
        },
        {
          prop: 'path',
          label: '请求路径',
          minWidth: 200,
          showOverflowTooltip: true
        },
        { prop: 'ip', label: 'IP', width: 140 },
        {
          prop: 'status_code',
          label: '状态码',
          width: 100,
          formatter: (row: OperationLogItem) => {
            return h(ElTag, { type: getStatusTagType(row.status_code) }, () => row.status_code)
          }
        },
        {
          prop: 'cost_time',
          label: '耗时(s)',
          width: 100,
          formatter: (row: OperationLogItem) => {
            const cost = row.cost_time.toFixed(2)
            return row.cost_time > 1 ? h('span', { style: 'color: #f56c6c' }, cost) : cost
          }
        },
        {
          prop: 'created_at',
          label: '操作时间',
          width: 180,
          sortable: true,
          formatter: (row: OperationLogItem) => {
            const date = new Date(row.created_at)
            const [datePart, timePart] = date.toLocaleString().split(' ')
            return `${datePart.replace(/\//g, '-')} ${timePart}`
          }
        }
      ]
    }
  })
</script>
