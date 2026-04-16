<script lang="ts" setup>
  import { Handle, Position, type NodeProps } from '@vue-flow/core'
  import { computed } from 'vue'

  interface NodeData {
    valueA: number
    valueB: number
    result: number
  }

  const props = defineProps<NodeProps<NodeData>>()

  const result = computed(() => (props.data.valueA ?? 0) + (props.data.valueB ?? 0))
</script>

<template>
  <div class="add-node">
    <div class="label">加法</div>
    <div class="values">
      <span>{{ props.data.valueA ?? 0 }}</span>
      <span>+</span>
      <span>{{ props.data.valueB ?? 0 }}</span>
    </div>
    <div class="result">= {{ result }}</div>
  </div>
  <Handle type="target" :position="Position.Left" id="a" :style="{ top: '30%' }" />
  <Handle type="target" :position="Position.Left" id="b" :style="{ top: '70%' }" />
  <Handle type="source" :position="Position.Right" id="output" />
</template>

<style scoped>
  .add-node {
    padding: 15px 20px;
    background: #fff3e0;
    border: 2px solid #f57c00;
    border-radius: 8px;
    min-width: 100px;
  }

  .label {
    font-weight: bold;
    color: #f57c00;
    margin-bottom: 8px;
  }

  .values {
    display: flex;
    gap: 8px;
    align-items: center;
    font-size: 14px;
  }

  .result {
    margin-top: 8px;
    font-weight: bold;
    color: #e65100;
  }
</style>