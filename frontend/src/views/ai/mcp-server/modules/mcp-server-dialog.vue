<template>
  <ElDialog
    v-model="dialogVisible"
    :title="type === 'add' ? '新增 MCP Server' : '编辑 MCP Server'"
    width="680px"
    align-center
  >
    <ElForm ref="formRef" :model="formData" :rules="rules" label-width="100px">
      <ElFormItem label="名称" prop="name">
        <ElInput v-model="formData.name" placeholder="请输入名称" />
      </ElFormItem>
      <ElFormItem label="编码" prop="code">
        <ElInput v-model="formData.code" placeholder="请输入编码" />
      </ElFormItem>
      <ElFormItem label="传输方式" prop="transport">
        <ElSelect v-model="formData.transport" placeholder="请选择传输方式" style="width: 100%">
          <ElOption label="SSE" value="sse" />
          <ElOption label="Streamable HTTP" value="streamable_http" />
          <ElOption label="Stdio" value="stdio" />
        </ElSelect>
      </ElFormItem>
      <ElFormItem label="地址" prop="url">
        <ElInput v-model="formData.url" placeholder="请输入连接地址" />
      </ElFormItem>
      <ElFormItem label="认证令牌" prop="auth_token">
        <ElInput
          v-model="formData.auth_token"
          type="password"
          show-password
          placeholder="请输入认证令牌（可选）"
        />
      </ElFormItem>
      <ElFormItem label="描述" prop="description">
        <ElInput
          v-model="formData.description"
          type="textarea"
          :rows="3"
          placeholder="请输入描述"
        />
      </ElFormItem>
      <ElFormItem label="状态" prop="status">
        <ElSwitch
          v-model="formData.status"
          :active-value="1"
          :inactive-value="0"
          active-text="启用"
          inactive-text="禁用"
        />
      </ElFormItem>

      <!-- 测试结果区域 -->
      <ElFormItem v-if="toolsList.length || toolsLoading">
        <div v-loading="toolsLoading" class="w-full">
          <div class="flex items-center justify-between mb-2">
            <span class="text-sm font-medium">可用工具（{{ toolsList.length }}）</span>
            <ElButton link size="small" @click="handleTest">重新测试</ElButton>
          </div>
          <div class="tools-list max-h-48 overflow-y-auto">
            <ElCard
              v-for="tool in toolsList"
              :key="tool.name"
              class="mb-2"
              shadow="hover"
              body-style="padding: 10px 14px"
            >
              <div class="font-medium text-sm">{{ tool.name }}</div>
              <div class="text-xs text-gray-400 mt-1">{{ tool.description || '暂无描述' }}</div>
            </ElCard>
          </div>
        </div>
      </ElFormItem>
    </ElForm>

    <template #footer>
      <div class="flex items-center justify-between">
        <ElButton :loading="toolsLoading" :disabled="!formData.id" @click="handleTest">
          <ri:flask-line class="mr-1" />测试连接
        </ElButton>
        <div>
          <ElButton @click="dialogVisible = false">取消</ElButton>
          <ElButton type="primary" :loading="submitting" @click="handleSubmit">提交</ElButton>
        </div>
      </div>
    </template>
  </ElDialog>
</template>

<script setup lang="ts">
  import type { FormInstance, FormRules } from 'element-plus'
  import { fetchAddMcpServer, fetchUpdateMcpServer, fetchTestMcpServer } from '@/api/ai'

  interface Props {
    visible: boolean
    type: string
    serverData?: Partial<Api.Ai.McpServerItem>
  }

  const props = withDefaults(defineProps<Props>(), {
    visible: false,
    type: 'add',
    serverData: () => ({})
  })

  const emit = defineEmits<{
    'update:visible': [value: boolean]
    submit: []
  }>()

  const dialogVisible = computed({
    get: () => props.visible,
    set: (v) => emit('update:visible', v)
  })

  const formRef = ref<FormInstance>()
  const submitting = ref(false)
  const toolsLoading = ref(false)
  const toolsList = ref<Api.Ai.McpServerTool[]>([])

  const formData = reactive({
    id: undefined as number | undefined,
    name: '',
    code: '',
    transport: 'sse',
    url: '',
    auth_token: '',
    description: '',
    status: 1
  })

  const rules: FormRules = {
    name: [{ required: true, message: '请输入名称', trigger: 'blur' }],
    code: [{ required: true, message: '请输入编码', trigger: 'blur' }],
    transport: [{ required: true, message: '请选择传输方式', trigger: 'change' }],
    url: [{ required: true, message: '请输入连接地址', trigger: 'blur' }]
  }

  // 弹窗打开时回填数据，重置测试状态
  watch(
    () => props.visible,
    (v) => {
      if (v) {
        const d = props.serverData
        formData.id = d.id
        formData.name = d.name || ''
        formData.code = d.code || ''
        formData.transport = d.transport || 'sse'
        formData.url = d.url || ''
        formData.auth_token = d.auth_token || ''
        formData.description = d.description || ''
        formData.status = d.status ?? 1
        toolsList.value = []
      }
    }
  )

  const handleSubmit = async () => {
    const valid = await formRef.value?.validate().catch(() => false)
    if (!valid) return

    submitting.value = true
    try {
      if (props.type === 'add') {
        await fetchAddMcpServer(formData)
        ElMessage.success('新增成功')
      } else {
        await fetchUpdateMcpServer(formData)
        ElMessage.success('编辑成功')
      }
      dialogVisible.value = false
      emit('submit')
    } finally {
      submitting.value = false
    }
  }

  const handleTest = async () => {
    if (!formData.id) {
      ElMessage.warning('请先保存后再测试')
      return
    }
    toolsLoading.value = true
    toolsList.value = []
    try {
      const res = await fetchTestMcpServer(formData.id)
      toolsList.value = Array.isArray(res) ? res : []
      if (!toolsList.value.length) {
        ElMessage.warning('连接成功，但未获取到可用工具')
      } else {
        ElMessage.success(`测试成功，共 ${toolsList.value.length} 个工具`)
      }
    } catch {
      ElMessage.error('测试失败，请检查配置是否正确')
    } finally {
      toolsLoading.value = false
    }
  }
</script>
