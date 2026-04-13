<script lang="ts" setup>
  // 可用节点类型列表
  const nodeTypes = [
    { type: 'number-input', label: '数值输入', color: '#1976d2', icon: '📝' },
    { type: 'add', label: '加法节点', color: '#f57c00', icon: '➕' },
    { type: 'result', label: '结果输出', color: '#388e3c', icon: '📊' }
  ]

  // 拖拽开始时记录节点类型
  function onDragStart(event: DragEvent, nodeType: string) {
    if (event.dataTransfer) {
      event.dataTransfer.setData('application/vueflow-node', nodeType)
      event.dataTransfer.setData('nodeType', nodeType)
      event.dataTransfer.effectAllowed = 'move'
    }
  }
</script>

<template>
  <div class="node-panel">
    <div class="panel-title">节点列表</div>
    <div class="node-list">
      <div
        v-for="node in nodeTypes"
        :key="node.type"
        class="node-item"
        :style="{ borderColor: node.color }"
        draggable="true"
        @dragstart="onDragStart($event, node.type)"
      >
        <span class="node-icon">{{ node.icon }}</span>
        <span class="node-label">{{ node.label }}</span>
      </div>
    </div>
    <div class="panel-tip">拖拽节点到画布</div>
  </div>
</template>

<style scoped>
  .node-panel {
    width: 200px;
    background: #f5f5f5;
    border-right: 1px solid #ddd;
    padding: 15px;
    display: flex;
    flex-direction: column;
  }

  .panel-title {
    font-size: 16px;
    font-weight: bold;
    margin-bottom: 15px;
    color: #333;
  }

  .node-list {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  .node-item {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 12px;
    background: #fff;
    border: 2px solid;
    border-radius: 8px;
    cursor: grab;
    transition: all 0.2s;
  }

  .node-item:hover {
    transform: scale(1.02);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  }

  .node-item:active {
    cursor: grabbing;
  }

  .node-icon {
    font-size: 18px;
  }

  .node-label {
    font-size: 14px;
    color: #333;
  }

  .panel-tip {
    margin-top: 15px;
    font-size: 12px;
    color: #999;
    text-align: center;
  }
</style>