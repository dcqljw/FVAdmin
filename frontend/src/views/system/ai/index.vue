<script setup lang="ts">
  import { fetchAiEdit } from '@/api/system-manage'

  const isEdit = ref(false)
  const model = reactive({
    baseUrl: '',
    name: '',
    apiKey: ''
  })
  const editHandler = () => {
    if (!isEdit.value) {
      fetchAiEdit(model).then((res) => {
        console.log(res)
      })
    }

    isEdit.value = !isEdit.value
  }
</script>

<template>
  <div class="art-full-height">
    <ElCard class="art-table-card" shadow="never">
      <ElForm :model="model" label-width="86px" label-position="top">
        <ElFormItem label="模型接口" prop="name">
          <ElInput v-model="model.baseUrl" :disabled="isEdit" />
        </ElFormItem>
        <ElFormItem label="模型名称" prop="name">
          <ElInput v-model="model.name" :disabled="isEdit" />
        </ElFormItem>
        <ElFormItem label="ApiKey" prop="apiKey">
          <ElInput type="password" v-model="model.apiKey" show-password :disabled="isEdit" />
        </ElFormItem>
        <el-button link>测试</el-button>
        <el-button type="primary" @click="editHandler">
          {{ isEdit ? '编辑' : '保存' }}
        </el-button>
      </ElForm>
    </ElCard>
  </div>
</template>
