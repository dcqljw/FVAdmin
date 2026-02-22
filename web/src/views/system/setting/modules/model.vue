<script setup lang="ts">
  import { useTable } from '@/hooks/core/useTable'
  import { useAuth } from '@/hooks'
  import { DialogType } from '@/types'
  import { fetchLLMList } from '@/api/system-manage'
  import ArtButtonTable from '@/components/core/forms/art-button-table/index.vue'
  import ArtSvgIcon from '@/components/core/base/art-svg-icon/index.vue'

  const dialogType = ref<DialogType>('add')
  const currentUserData = ref({})
  const dialogVisible = ref(false)
  const { hasAuth } = useAuth()

  // 在组件中定义响应式状态
  const visibleMap = ref<Map<number, boolean>>(new Map())

  // 切换显示状态
  const toggleVisible = (row: any) => {
    const current = visibleMap.value.get(row.id) || false
    visibleMap.value.set(row.id, !current)
    // 触发更新（Vue 3 Map 需要重新赋值）
    visibleMap.value = new Map(visibleMap.value)
  }

  const { columns, columnChecks, data, loading, pagination, refreshData } = useTable({
    core: {
      apiFn: fetchLLMList,
      columnsFactory: () => [
        {
          prop: 'name',
          label: 'Name',
          width: 100
        },
        {
          prop: 'base_url',
          label: 'baseUrl'
        },
        {
          prop: 'model',
          label: 'model'
        },
        {
          prop: 'api_key',
          label: 'apiKey',
          width: 300,
          formatter: (row) => {
            const isVisible = visibleMap.value.get(row.id)
            return h('div', { class: 'flex items-center gap-1 cursor-pointer justify-between' }, [
              h(
                'span',
                { class: 'flex-1 overflow-x-auto whitespace-nowrap scrollbar-thin' },
                isVisible ? row.api_key : '*********'
              ),
              h(
                'span',
                {
                  onClick: (e: Event) => {
                    e.stopPropagation()
                    toggleVisible(row)
                  }
                },
                [
                  h(ArtSvgIcon, {
                    icon: isVisible ? 'ri:eye-line' : 'ri:eye-off-line'
                  })
                ]
              )
            ])
          }
        },
        {
          prop: 'operation',
          label: '操作',
          width: 180,
          fixed: 'right',
          formatter: () =>
            h('div', [
              h(ArtButtonTable, {
                type: 'edit',
                onClick: () => {}
              }),
              h(ArtButtonTable, {
                type: 'delete',
                onClick: () => {}
              })
            ])
        }
      ]
    }
  })
  const showDialog = (type: DialogType, row?: any): void => {
    console.log('打开弹窗:', { type, row })
    dialogType.value = type
    currentUserData.value = row || {}
    nextTick(() => {
      dialogVisible.value = true
    })
  }
</script>

<template>
  <div class="">
    <ArtTableHeader v-model:columns="columnChecks" :loading="loading" @refresh="refreshData">
      <template #left>
        <ElSpace wrap>
          <ElButton v-if="hasAuth('user:add')" @click="showDialog('add')" v-ripple
            >新增用户</ElButton
          >
        </ElSpace>
      </template>
    </ArtTableHeader>
    <ArtTable :loading="loading" :data="data" :columns="columns" :pagination="pagination">
    </ArtTable>
  </div>
</template>

<style scoped lang="scss"></style>
