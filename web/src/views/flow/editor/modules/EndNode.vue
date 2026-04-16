<script lang="ts" setup>
  import { Handle, Position, type NodeProps } from '@vue-flow/core'

  interface NodeData {
    label: string
    outputVar: string
    outputType: string
    returnType: string
  }

  defineProps<NodeProps<NodeData>>()
</script>

<template>
  <Handle type="target" :position="Position.Left" id="input" />
  <div class="end-node">
    <div class="node-header">
      <div class="icon-wrapper">
        <svg class="icon" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path
            d="M12 8H4M4 8L7.5 4.5M4 8L7.5 11.5"
            stroke="white"
            stroke-width="1.5"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
        </svg>
      </div>
      <span class="title">结束</span>
    </div>
    <div class="node-body">
      <div class="field-row">
        <span class="field-label">输出</span>
        <span class="field-type">str</span>
        <span class="field-name">{{ data.outputVar ?? 'output' }}</span>
      </div>
      <div class="field-row">
        <span class="field-label">输出类型</span>
        <span class="field-value">{{ data.returnType ?? '返回变量' }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
  .end-node {
    min-width: 200px;
    background: linear-gradient(135deg, #f8f9ff, #f0f2ff);
    border: 1px solid #d0d4f0;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(80, 100, 200, 0.08);
    overflow: hidden;
  }

  .node-header {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 14px;
    background: linear-gradient(135deg, #6366f1, #818cf8);
  }

  .icon-wrapper {
    width: 20px;
    height: 20px;
    background: rgba(255, 255, 255, 0.25);
    border-radius: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .icon {
    width: 14px;
    height: 14px;
  }

  .title {
    font-size: 14px;
    font-weight: 600;
    color: #fff;
  }

  .node-body {
    padding: 10px 14px;
    display: flex;
    flex-direction: column;
    gap: 6px;
  }

  .field-row {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 12px;
  }

  .field-label {
    color: #8b8fa3;
  }

  .field-type {
    background: #e8eaf6;
    color: #6366f1;
    padding: 1px 6px;
    border-radius: 3px;
    font-size: 11px;
  }

  .field-name {
    color: #4a4e69;
    font-weight: 500;
  }

  .field-value {
    color: #4a4e69;
    font-weight: 500;
  }
</style>
