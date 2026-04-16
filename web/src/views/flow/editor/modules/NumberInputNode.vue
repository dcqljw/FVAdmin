<script lang="ts" setup>
  import { Handle, Position, type NodeProps } from '@vue-flow/core'

  interface NodeData {
    value: number
    label: string
  }

  const props = defineProps<NodeProps<NodeData>>()

  function onInput(event: Event) {
    const target = event.target as HTMLInputElement
    props.data.value = Number(target.value) || 0
  }
</script>

<template>
  <div class="number-input-node">
    <div class="label">{{ props.data.label }}</div>
    <input type="number" :value="props.data.value ?? 0" @input="onInput" class="input" />
  </div>
  <Handle type="source" :position="Position.Right" id="output" />
</template>

<style scoped>
  .number-input-node {
    padding: 10px 15px;
    background: #e3f2fd;
    border: 2px solid #1976d2;
    border-radius: 8px;
    min-width: 80px;
  }

  .label {
    font-weight: bold;
    margin-bottom: 5px;
    color: #1976d2;
  }

  .input {
    width: 60px;
    padding: 4px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
</style>
