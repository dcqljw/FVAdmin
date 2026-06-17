<script lang="ts" setup>
  import { Handle, Position, type NodeProps } from '@vue-flow/core'
  import { NodeToolbar } from '@vue-flow/node-toolbar'

  interface NodeData {
    label: string
    toolbarVisible: boolean
    toolbarPosition: Position
  }

  const props = defineProps<NodeProps<NodeData>>()
</script>

<template>
  <NodeToolbar :is-visible="props.data.toolbarVisible" :position="props.data.toolbarPosition">
    <button>删除</button>
    <button>复制</button>
    <button>展开</button>
  </NodeToolbar>

  <div class="custom-node">
    {{ props.data.label }}
  </div>

  <Handle type="target" :position="Position.Left" />
  <Handle type="source" :position="Position.Right" />
</template>

<style scoped>
  .custom-node {
    padding: 10px 20px;
    background: #fff;
    border: 1px solid #ddd;
    border-radius: 4px;
  }
</style>
