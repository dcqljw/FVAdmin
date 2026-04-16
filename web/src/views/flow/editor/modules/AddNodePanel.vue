<script lang="ts" setup>
  import { ElDrawer } from 'element-plus'

  const visible = defineModel<boolean>('visible', { required: true })

  const emit = defineEmits<{
    add: [type: string]
  }>()

  const nodeTypes = [
    { type: 'start', label: '开始', color: '#6366f1', icon: '▶' },
    { type: 'end', label: '结束', color: '#6366f1', icon: '◼' },
    { type: 'number-input', label: '数值输入', color: '#1976d2', icon: '📝' },
    { type: 'add', label: '加法', color: '#f57c00', icon: '➕' },
    { type: 'result', label: '结果输出', color: '#388e3c', icon: '📊' }
  ]

  function handleAdd(type: string) {
    emit('add', type)
    visible.value = false
  }
</script>

<template>
  <ElDrawer v-model="visible" direction="btt" size="200px" :with-header="false" class="add-node-panel">
    <div class="panel-title">添加节点</div>
    <div class="node-list">
      <div
        v-for="node in nodeTypes"
        :key="node.type"
        class="node-item"
        @click="handleAdd(node.type)"
      >
        <span class="node-icon">{{ node.icon }}</span>
        <span class="node-label">{{ node.label }}</span>
      </div>
    </div>
  </ElDrawer>
</template>

<style scoped>
  .panel-title {
    font-size: 16px;
    font-weight: 600;
    color: #333;
    text-align: center;
    margin-bottom: 16px;
  }

  .node-list {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
  }

  .node-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 6px;
    padding: 16px 8px;
    background: #f8f9ff;
    border: 1px solid #e0e2f0;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s;
  }

  .node-item:hover {
    border-color: #6366f1;
    background: #f0f2ff;
    box-shadow: 0 2px 8px rgba(99, 102, 241, 0.12);
  }

  .node-icon {
    font-size: 20px;
  }

  .node-label {
    font-size: 12px;
    color: #4a4e69;
  }
</style>
