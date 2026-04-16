<!-- 工作流列表页面 -->
<!-- art-full-height 自动计算出页面剩余高度 -->
<!-- art-table-card 一个符合系统样式的 class，同时自动撑满剩余高度 -->
<template>
  <div class="flow-list-page art-full-height">
    <ElCard class="art-table-card" shadow="never">
      <!-- 表格头部 -->
      <ArtTableHeader v-model:columns="columnChecks" :loading="loading" @refresh="refreshData">
        <template #left>
          <ElSpace wrap>
            <ElButton type="primary" @click="handleCreate" v-ripple>新建工作流</ElButton>
          </ElSpace>
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
    </ElCard>
  </div>
</template>

<script setup lang="ts">
  import { h } from 'vue'
  import { useRouter } from 'vue-router'
  import ArtTableHeader from '@/components/core/tables/art-table-header/index.vue'
  import { useTable } from '@/hooks/core/useTable'
  import { ElButton, ElDropdown, ElDropdownMenu, ElDropdownItem } from 'element-plus'

  const router = useRouter()

  defineOptions({ name: 'FlowList' })

  // 模拟工作流列表数据（写死）
  const mockFlowList = [
    {
      id: 'default',
      name: 'test',
      desc: 'test',
      type: '工作流',
      updateTime: '2026-04-16 20:47',
      status: 'published'
    }
  ]

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
      apiFn: async () => {
        // 模拟异步请求
        return Promise.resolve({
          list: mockFlowList,
          total: mockFlowList.length
        })
      },
      apiParams: { current: 1, size: 20 },
      columnsFactory: () => [
        {
          prop: 'name',
          label: '资源',
          minWidth: 200,
          visible: true,
          formatter: (row) => {
            return h('div', { style: 'min-width: 0' }, [
              h('div', { style: 'display: flex; align-items: center; gap: 4px' }, [
                h('span', { style: 'font-size: 14px; font-weight: 500; color: #333' }, row.name),
                row.status === 'published'
                  ? h(
                      'svg',
                      {
                        viewBox: '0 0 16 16',
                        width: '14',
                        height: '14',
                        fill: 'none',
                        style: 'display: inline-flex'
                      },
                      [
                        h('circle', { cx: '8', cy: '8', r: '7', fill: '#22c55e' }),
                        h('path', {
                          d: 'M5.5 8L7 9.5L10.5 6',
                          stroke: 'white',
                          'stroke-width': '1.5',
                          'stroke-linecap': 'round',
                          'stroke-linejoin': 'round'
                        })
                      ]
                    )
                  : null
              ]),
              h('p', { style: 'font-size: 12px; color: #999; margin-top: 2px' }, row.desc)
            ])
          }
        },
        { prop: 'updateTime', label: '编辑时间', width: 200, visible: true },
        {
          prop: 'action',
          label: '操作',
          width: 80,
          visible: true,
          formatter: (row) => {
            return h(
              ElDropdown,
              {
                trigger: 'click',
                onCommand: (command: string) => handleAction(command, row)
              },
              {
                default: () =>
                  h(
                    'span',
                    {
                      style:
                        'font-size: 18px; color: #999; cursor: pointer; padding: 4px 8px; border-radius: 4px'
                    },
                    '···'
                  ),
                dropdown: () =>
                  h(ElDropdownMenu, {}, () => [
                    h(ElDropdownItem, { command: 'edit' }, () => '编辑'),
                    h(ElDropdownItem, { command: 'copy' }, () => '复制'),
                    h(ElDropdownItem, { command: 'delete', divided: true }, () => '删除')
                  ])
              }
            )
          }
        }
      ]
    }
  })

  function handleCreate() {
    // TODO: 新建工作流
  }

  function handleAction(command: string, row: any) {
    switch (command) {
      case 'edit':
        router.push(`/flow/editor/${row.id}`)
        break
      case 'copy':
        // TODO: 复制工作流
        break
      case 'delete':
        // TODO: 删除工作流
        break
    }
  }
</script>
