<!-- MCP Server 管理页面 -->
<template>
  <div class="art-full-height">
    <ElCard class="art-table-card" shadow="never">
      <!-- 表格头部 -->
      <ArtTableHeader v-model:columns="columnChecks" :loading="loading" @refresh="refreshData">
        <template #left>
          <ElButton @click="showDialog('add')">新增 MCP Server</ElButton>
        </template>
      </ArtTableHeader>

      <!-- 表格 -->
      <ArtTable
        :loading="loading"
        :data="data"
        :columns="columns"
        :pagination="pagination"
        @pagination:size-change="handleSizeChange"
        @pagination:current-change="handleCurrentChange"
      />

      <!-- 新增/编辑弹窗 -->
      <McpServerDialog
        v-model:visible="dialogVisible"
        :type="dialogType"
        :server-data="currentServerData"
        @submit="refreshData"
      />
    </ElCard>
  </div>
</template>

<script setup lang="ts">
  import { h } from 'vue'
  import { ElTag, ElMessageBox } from 'element-plus'
  import ArtButtonTable from '@/components/core/forms/art-button-table/index.vue'
  import { useTable } from '@/hooks/core/useTable'
  import { fetchGetMcpServerList, fetchDeleteMcpServer } from '@/api/ai'
  import { DialogType } from '@/types'
  import McpServerDialog from './modules/mcp-server-dialog.vue'

  defineOptions({ name: 'McpServer' })

  type McpServerItem = Api.Ai.McpServerItem

  const dialogType = ref<DialogType>('add')
  const dialogVisible = ref(false)
  const currentServerData = ref<Partial<McpServerItem>>({})

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
      apiFn: fetchGetMcpServerList,
      apiParams: { current: 1, size: 20 },
      columnsFactory: () => [
        { type: 'index', width: 60, label: '序号' },
        { prop: 'name', label: '名称', minWidth: 120 },
        { prop: 'code', label: '编码', minWidth: 120 },
        { prop: 'transport', label: '传输方式', width: 130 },
        { prop: 'url', label: '连接地址', minWidth: 220, showOverflowTooltip: true },
        { prop: 'description', label: '描述', minWidth: 180, showOverflowTooltip: true },
        {
          prop: 'status',
          label: '状态',
          width: 100,
          formatter: (row: McpServerItem) => {
            const config =
              row.status === 1
                ? { type: 'success' as const, text: '启用' }
                : { type: 'danger' as const, text: '禁用' }
            return h(ElTag, { type: config.type }, () => config.text)
          }
        },
        {
          prop: 'created_at',
          label: '创建时间',
          width: 180,
          sortable: true
        },
        {
          prop: 'operation',
          label: '操作',
          width: 140,
          fixed: 'right',
          formatter: (row: McpServerItem) =>
            h('div', [
              h(ArtButtonTable, {
                type: 'edit',
                onClick: () => showDialog('edit', row)
              }),
              h(ArtButtonTable, {
                type: 'delete',
                onClick: () => deleteServer(row)
              })
            ])
        }
      ]
    }
  })

  const showDialog = (type: DialogType, row?: McpServerItem) => {
    dialogType.value = type
    currentServerData.value = row || {}
    nextTick(() => {
      dialogVisible.value = true
    })
  }

  const deleteServer = (row: McpServerItem) => {
    ElMessageBox.confirm(`确定要删除「${row.name}」吗？`, '删除确认', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }).then(() => {
      fetchDeleteMcpServer(row.id).then(() => {
        ElMessage.success('删除成功')
        refreshData()
      })
    })
  }
</script>
