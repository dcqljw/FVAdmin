<script setup lang="ts">
  import { ref } from 'vue'
  import Model from '@views/system/setting/modules/model.vue'

  const currentTab = ref('model')
</script>

<template>
  <div class="art-full-height">
    <ElCard class="art-table-card" shadow="never">
      <el-tabs v-model="currentTab">
        <el-tab-pane label="模型管理" name="model">
          <Model />
        </el-tab-pane>
        <el-tab-pane label="Settings">1</el-tab-pane>
        <el-tab-pane label="Settings">1</el-tab-pane>
        <el-tab-pane label="Settings">1</el-tab-pane>
      </el-tabs>
    </ElCard>
  </div>
</template>
