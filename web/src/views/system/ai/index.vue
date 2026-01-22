<script setup lang="ts">
  const model = reactive({
    name: '',
    apiKey: ''
  })
</script>

<template>
  <div class="art-full-height">
    <ElCard class="art-table-card" shadow="never">
      <ElForm :model="model" label-width="86px" label-position="top">
        <ElFormItem label="模型名称" prop="name">
          <ElInput v-model="model.name" />
        </ElFormItem>
        <ElFormItem label="ApiKey" prop="apiKey">
          <ElInput type="password" v-model="model.apiKey" show-password />
        </ElFormItem>
      </ElForm>
    </ElCard>
  </div>
</template>
