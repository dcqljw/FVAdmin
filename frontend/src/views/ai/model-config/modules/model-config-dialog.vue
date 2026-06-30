<template>
  <ElDialog
    v-model="dialogVisible"
    :title="type === 'add' ? '新增模型配置' : '编辑模型配置'"
    width="680px"
    align-center
  >
    <ElForm ref="formRef" :model="formData" :rules="rules" label-width="110px">
      <ElFormItem label="模型名称" prop="name">
        <ElInput v-model="formData.name" placeholder="请输入模型名称" />
      </ElFormItem>
      <ElFormItem label="唯一编码" prop="code">
        <ElInput v-model="formData.code" placeholder="请输入唯一编码" :disabled="type === 'edit'" />
      </ElFormItem>
      <ElFormItem label="提供商" prop="provider">
        <ElInput v-model="formData.provider" placeholder="请输入提供商（如 OpenAI、DeepSeek）" />
      </ElFormItem>
      <ElFormItem label="API 地址" prop="base_url">
        <ElInput v-model="formData.base_url" placeholder="请输入 API Base URL" />
      </ElFormItem>
      <ElFormItem label="API Key" prop="api_key">
        <ElInput
          v-model="formData.api_key"
          type="password"
          show-password
          :placeholder="type === 'edit' ? '留空表示不修改' : '请输入 API Key'"
        />
      </ElFormItem>
      <ElFormItem label="模型标识" prop="model_name">
        <ElInput v-model="formData.model_name" placeholder="请输入模型标识（如 gpt-4o、deepseek-chat）" />
      </ElFormItem>
      <ElFormItem label="最大 Tokens" prop="max_tokens">
        <ElInputNumber v-model="formData.max_tokens" :min="1" :max="1000000" style="width: 100%" />
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
      <ElFormItem label="默认模型" prop="is_default">
        <ElSwitch v-model="formData.is_default" active-text="是" inactive-text="否" />
      </ElFormItem>
    </ElForm>

    <template #footer>
      <ElButton @click="dialogVisible = false">取消</ElButton>
      <ElButton type="primary" :loading="submitting" @click="handleSubmit">提交</ElButton>
    </template>
  </ElDialog>
</template>

<script setup lang="ts">
  import type { FormInstance, FormRules } from 'element-plus'
  import { fetchAddModelConfig, fetchUpdateModelConfig } from '@/api/ai'

  interface Props {
    visible: boolean
    type: string
    modelData?: Partial<Api.Ai.ModelConfigItem>
  }

  const props = withDefaults(defineProps<Props>(), {
    visible: false,
    type: 'add',
    modelData: () => ({})
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

  const formData = reactive({
    id: undefined as number | undefined,
    name: '',
    code: '',
    provider: '',
    base_url: '',
    api_key: '',
    model_name: '',
    max_tokens: 2048,
    is_default: false,
    status: 1
  })

  const rules: FormRules = {
    name: [{ required: true, message: '请输入模型名称', trigger: 'blur' }],
    code: [{ required: true, message: '请输入唯一编码', trigger: 'blur' }],
    base_url: [{ required: true, message: '请输入 API 地址', trigger: 'blur' }],
    api_key: [
      {
        required: true,
        message: '请输入 API Key',
        trigger: 'blur',
        validator: (_rule, value, callback) => {
          if (props.type === 'add' && !value) {
            callback(new Error('请输入 API Key'))
          } else {
            callback()
          }
        }
      }
    ],
    model_name: [{ required: true, message: '请输入模型标识', trigger: 'blur' }]
  }

  watch(
    () => props.visible,
    (v) => {
      if (v) {
        const d = props.modelData
        formData.id = d.id
        formData.name = d.name || ''
        formData.code = d.code || ''
        formData.provider = d.provider || ''
        formData.base_url = d.base_url || ''
        formData.api_key = d.api_key || ''
        formData.model_name = d.model_name || ''
        formData.max_tokens = d.max_tokens ?? 2048
        formData.is_default = d.is_default ?? false
        formData.status = d.status ?? 1
      }
    }
  )

  const handleSubmit = async () => {
    const valid = await formRef.value?.validate().catch(() => false)
    if (!valid) return

    submitting.value = true
    try {
      if (props.type === 'add') {
        await fetchAddModelConfig({ ...formData })
        ElMessage.success('新增成功')
      } else {
        const { id, name, code, provider, base_url, model_name, max_tokens, is_default, status } =
          formData
        const submitData: Partial<Api.Ai.ModelConfigItem> = {
          id,
          name,
          code,
          provider,
          base_url,
          model_name,
          max_tokens,
          is_default,
          status
        }
        if (formData.api_key) {
          submitData.api_key = formData.api_key
        }
        await fetchUpdateModelConfig(submitData)
        ElMessage.success('编辑成功')
      }
      dialogVisible.value = false
      emit('submit')
    } finally {
      submitting.value = false
    }
  }
</script>
