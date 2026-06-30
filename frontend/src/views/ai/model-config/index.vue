<!-- 模型配置管理页面 -->
<template>
  <div class="art-full-height">
    <!-- 搜索栏 -->
    <ArtSearchBar
      v-model="searchForm"
      :items="searchItems"
      :showExpand="false"
      @search="handleSearch"
      @reset="resetSearchParams"
    />

    <ElCard class="art-table-card" shadow="never">
      <!-- 表格头部 -->
      <ArtTableHeader v-model:columns="columnChecks" :loading="loading" @refresh="refreshData">
        <template #left>
          <ElButton @click="showDialog('add')">新增模型</ElButton>
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
      <ModelConfigDialog
        v-model:visible="dialogVisible"
        :type="dialogType"
        :model-data="currentModelData"
        @submit="refreshData"
      />
    </ElCard>
  </div>
</template>

<script setup lang="ts">
  import { h } from 'vue'
  import { ElTag, ElMessageBox } from 'element-plus'
  import ArtButtonTable from '@/components/core/forms/art-button-table/index.vue'
  import ArtSearchBar from '@/components/core/forms/art-search-bar/index.vue'
  import { useTable } from '@/hooks/core/useTable'
  import { fetchGetModelConfigList, fetchDeleteModelConfig } from '@/api/ai'
  import { DialogType } from '@/types'
  import ModelConfigDialog from './modules/model-config-dialog.vue'

  defineOptions({ name: 'ModelConfig' })

  type ModelConfigItem = Api.Ai.ModelConfigItem

  const dialogType = ref<DialogType>('add')
  const dialogVisible = ref(false)
  const currentModelData = ref<Partial<ModelConfigItem>>({})

  const searchForm = ref({
    name: undefined as string | undefined,
    status: undefined as number | undefined
  })

  const searchItems = [
    {
      label: '模型名称',
      key: 'name',
      type: 'input',
      placeholder: '请输入模型名称',
      clearable: true
    },
    {
      label: '状态',
      key: 'status',
      type: 'select',
      props: {
        placeholder: '请选择状态',
        options: [
          { label: '启用', value: 1 },
          { label: '禁用', value: 0 }
        ]
      }
    }
  ]

  const handleSearch = () => {
    Object.assign(searchParams, searchForm.value)
    getData()
  }

  const {
    columns,
    columnChecks,
    data,
    loading,
    pagination,
    getData,
    searchParams,
    resetSearchParams,
    handleSizeChange,
    handleCurrentChange,
    refreshData
  } = useTable({
    core: {
      apiFn: fetchGetModelConfigList,
      apiParams: { current: 1, size: 20, ...searchForm.value },
      columnsFactory: () => [
        { type: 'index', width: 60, label: '序号' },
        { prop: 'name', label: '模型名称', minWidth: 120 },
        { prop: 'code', label: '编码', minWidth: 100 },
        { prop: 'provider', label: '提供商', minWidth: 100 },
        { prop: 'model_name', label: '模型标识', minWidth: 130 },
        { prop: 'base_url', label: 'API 地址', minWidth: 200, showOverflowTooltip: true },
        { prop: 'max_tokens', label: '最大 Tokens', width: 110 },
        {
          prop: 'is_default',
          label: '默认',
          width: 80,
          formatter: (row: ModelConfigItem) =>
            row.is_default
              ? h(ElTag, { type: 'warning' as const, size: 'small' }, () => '默认')
              : null
        },
        {
          prop: 'status',
          label: '状态',
          width: 90,
          formatter: (row: ModelConfigItem) => {
            const config =
              row.status === 1
                ? { type: 'success' as const, text: '启用' }
                : { type: 'danger' as const, text: '禁用' }
            return h(ElTag, { type: config.type, size: 'small' }, () => config.text)
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
          formatter: (row: ModelConfigItem) =>
            h('div', [
              h(ArtButtonTable, {
                type: 'edit',
                onClick: () => showDialog('edit', row)
              }),
              h(ArtButtonTable, {
                type: 'delete',
                onClick: () => deleteModel(row)
              })
            ])
        }
      ]
    }
  })

  const showDialog = (type: DialogType, row?: ModelConfigItem) => {
    dialogType.value = type
    currentModelData.value = row || {}
    nextTick(() => {
      dialogVisible.value = true
    })
  }

  const deleteModel = (row: ModelConfigItem) => {
    ElMessageBox.confirm(`确定要删除模型「${row.name}」吗？`, '删除确认', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }).then(() => {
      fetchDeleteModelConfig(row.id).then(() => {
        ElMessage.success('删除成功')
        refreshData()
      })
    })
  }
</script>
