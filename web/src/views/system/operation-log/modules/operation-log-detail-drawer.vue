<!-- 操作日志详情抽屉 -->
<template>
  <ElDrawer
    v-model="drawerVisible"
    title="操作日志详情"
    size="500px"
    :destroy-on-close="true"
  >
    <ElDescriptions :column="2" border>
      <ElDescriptionsItem label="ID">{{ logData.id }}</ElDescriptionsItem>
      <ElDescriptionsItem label="用户名">{{ logData.username }}</ElDescriptionsItem>
      <ElDescriptionsItem label="操作模块" :span="2">{{ logData.module }}</ElDescriptionsItem>
      <ElDescriptionsItem label="操作类型" :span="2">
        <ElTag :type="getOperationTagType(logData.operation)">{{ logData.operation }}</ElTag>
      </ElDescriptionsItem>
      <ElDescriptionsItem label="请求方法">
        <ElTag :type="getMethodTagType(logData.method)">{{ logData.method }}</ElTag>
      </ElDescriptionsItem>
      <ElDescriptionsItem label="状态码">
        <ElTag :type="getStatusTagType(logData.status_code)">{{ logData.status_code }}</ElTag>
      </ElDescriptionsItem>
      <ElDescriptionsItem label="请求路径" :span="2">
        <span style="word-break: break-all">{{ logData.path }}</span>
      </ElDescriptionsItem>
      <ElDescriptionsItem label="IP 地址">{{ logData.ip }}</ElDescriptionsItem>
      <ElDescriptionsItem label="耗时(s)">{{ logData.cost_time.toFixed(2) }}</ElDescriptionsItem>
      <ElDescriptionsItem label="操作时间" :span="2">{{ formatTime(logData.created_at) }}</ElDescriptionsItem>
    </ElDescriptions>

    <div v-if="logData.query_params" class="detail-section">
      <div class="detail-label">查询参数</div>
      <ElInput
        type="textarea"
        :model-value="formattedQueryParams"
        :autosize="{ minRows: 2, maxRows: 8 }"
        readonly
      />
    </div>

    <div v-if="logData.request_body" class="detail-section">
      <div class="detail-label">请求体</div>
      <ElInput
        type="textarea"
        :model-value="formattedRequestBody"
        :autosize="{ minRows: 2, maxRows: 8 }"
        readonly
      />
    </div>
  </ElDrawer>
</template>

<script setup lang="ts">
  import { ElDescriptions, ElDescriptionsItem, ElDrawer, ElInput, ElTag } from 'element-plus'
  import { getStatusTagType, getMethodTagType, getOperationTagType, formatJson } from '../utils'

  interface Props {
    modelValue: boolean
    logData: Api.OperationLog.OperationLogItem
  }

  interface Emits {
    (e: 'update:modelValue', value: boolean): void
  }

  const props = defineProps<Props>()
  const emit = defineEmits<Emits>()

  const drawerVisible = computed({
    get: () => props.modelValue,
    set: (value) => emit('update:modelValue', value)
  })

  const formatTime = (time: string) => {
    if (!time) return ''
    const date = new Date(time)
    const [datePart, timePart] = date.toLocaleString().split(' ')
    return `${datePart.replace(/\//g, '-')} ${timePart}`
  }

  const formattedQueryParams = computed(() => formatJson(props.logData.query_params))
  const formattedRequestBody = computed(() => formatJson(props.logData.request_body))
</script>

<style scoped lang="scss">
  .detail-section {
    margin-top: 16px;

    .detail-label {
      font-weight: 600;
      margin-bottom: 8px;
    }
  }
</style>
