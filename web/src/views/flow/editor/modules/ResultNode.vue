<script lang="ts" setup>
  import { Handle, Position, type NodeProps } from '@vue-flow/core'

  interface NodeData {
    result: number
  }

  const props = defineProps<NodeProps<NodeData>>()
</script>

<template>
  <div class="result-node">
    <div class="label">结果</div>
    <div class="value">{{ props.data.result ?? 0 }}</div>
  </div>
  <Handle type="target" :position="Position.Left" id="input" />
</template>

<style scoped>
  .result-node {
    padding: 15px 20px;
    background: #e8f5e9;
    border: 2px solid #388e3c;
    border-radius: 8px;
    min-width: 80px;
  }

  .label {
    font-weight: bold;
    color: #388e3c;
    margin-bottom: 8px;
  }

  .value {
    font-size: 24px;
    font-weight: bold;
    color: #2e7d32;
  }
</style>