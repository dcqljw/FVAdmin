<script setup lang="ts">
  import { ref, watch } from 'vue'
  import type { Node, Edge, Connection } from '@vue-flow/core'
  import { VueFlow, useVueFlow } from '@vue-flow/core'
  import { Controls } from '@vue-flow/controls'

  // 自定义节点组件
  import NumberInputNode from './modules/NumberInputNode.vue'
  import AddNode from './modules/AddNode.vue'
  import ResultNode from './modules/ResultNode.vue'
  import NodePanel from './modules/NodePanel.vue'

  // VueFlow hooks
  const { project, addEdges } = useVueFlow()

  // 节点数据
  const nodes = ref<Node[]>([])

  // 边数据
  const edges = ref<Edge[]>([])

  // 生成唯一 id
  function generateId() {
    return `node-${Date.now()}-${Math.random().toString(36).slice(2, 6)}`
  }

  // 获取节点默认数据
  function getDefaultData(type: string) {
    switch (type) {
      case 'number-input':
        return { label: '数值', value: 0 }
      case 'add':
        return { valueA: 0, valueB: 0, result: 0 }
      case 'result':
        return { result: 0 }
      default:
        return {}
    }
  }

  // 处理连线
  function onConnect(connection: Connection) {
    addEdges([
      {
        id: `edge-${Date.now()}`,
        source: connection.source,
        target: connection.target,
        sourceHandle: connection.sourceHandle,
        targetHandle: connection.targetHandle
      }
    ])
  }

  // 处理拖拽放置
  function onDrop(event: DragEvent) {
    const nodeType = event.dataTransfer?.getData('nodeType')
    if (!nodeType) return

    event.preventDefault()

    // 获取 VueFlow 容器的位置
    const bounds = (event.target as HTMLElement).closest('.vue-flow')?.getBoundingClientRect()
    if (!bounds) return

    const x = event.clientX - bounds.left
    const y = event.clientY - bounds.top

    // 转换为画布坐标
    const position = project({ x, y })

    // 添加新节点
    const newNode: Node = {
      id: generateId(),
      type: nodeType,
      position,
      data: getDefaultData(nodeType)
    }

    nodes.value = [...nodes.value, newNode]
  }

  // 只在拖拽节点时阻止默认行为
  function onDragOver(event: DragEvent) {
    event.preventDefault()
    if (event.dataTransfer) {
      event.dataTransfer.dropEffect = 'move'
    }
  }

  // 根据连线计算数据流动
  function calculateData() {
    // 找到所有 add 节点
    const addNodes = nodes.value.filter((n) => n.type === 'add')

    for (const addNode of addNodes) {
      // 找到连接到 addNode 的边
      const connectedEdges = edges.value.filter((e) => e.target === addNode.id)

      // 获取输入节点的值
      let valueA = 0
      let valueB = 0

      for (const edge of connectedEdges) {
        const sourceNode = nodes.value.find((n) => n.id === edge.source)
        if (sourceNode?.type === 'number-input') {
          const value = sourceNode.data.value ?? 0
          // 根据 targetHandle 区分两个输入
          if (edge.targetHandle === 'a') {
            valueA = value
          } else if (edge.targetHandle === 'b') {
            valueB = value
          } else {
            // 没有 handle 区分时，按顺序赋值
            if (valueA === 0) valueA = value
            else valueB = value
          }
        } else if (sourceNode?.type === 'add') {
          // 如果连接的是另一个 add 节点，用它的结果
          const value = sourceNode.data.result ?? 0
          if (valueA === 0) valueA = value
          else valueB = value
        }
      }

      // 更新 add 节点数据
      addNode.data.valueA = valueA
      addNode.data.valueB = valueB
      addNode.data.result = valueA + valueB
    }

    // 找到所有 result 节点并更新
    const resultNodes = nodes.value.filter((n) => n.type === 'result')
    for (const resultNode of resultNodes) {
      const connectedEdge = edges.value.find((e) => e.target === resultNode.id)
      if (connectedEdge) {
        const sourceNode = nodes.value.find((n) => n.id === connectedEdge.source)
        if (sourceNode) {
          resultNode.data.result = sourceNode.data.result ?? sourceNode.data.value ?? 0
        }
      }
    }
  }

  // 监听节点和边变化，触发计算
  watch([nodes, edges], calculateData, { deep: true })
</script>

<template>
  <ElCard class="art-table-card" shadow="never">
    <div class="flow-wrapper">
      <!-- 左侧节点面板 -->
      <NodePanel />

      <!-- 右侧画布 -->
      <div class="flow-canvas">
        <VueFlow
          v-model:nodes="nodes"
          v-model:edges="edges"
          @connect="onConnect"
          @drop="onDrop"
          @dragover="onDragOver"
        >
          <Controls position="top-right" />

          <!-- 数值输入节点 -->
          <template #node-number-input="nodeProps">
            <NumberInputNode v-bind="nodeProps" />
          </template>

          <!-- 加法节点 -->
          <template #node-add="nodeProps">
            <AddNode v-bind="nodeProps" />
          </template>

          <!-- 结果节点 -->
          <template #node-result="nodeProps">
            <ResultNode v-bind="nodeProps" />
          </template>
        </VueFlow>
      </div>
    </div>
  </ElCard>
</template>

<style>
  @import '@vue-flow/core/dist/style.css';
  @import '@vue-flow/core/dist/theme-default.css';
  @import '@vue-flow/controls/dist/style.css';
</style>

<style scoped>
  .art-table-card {
    height: calc(100vh - 120px);
    position: relative;
  }

  .art-table-card :deep(.el-card__body) {
    height: 100%;
    padding: 0;
  }

  .flow-wrapper {
    display: flex;
    height: 100%;
  }

  .flow-canvas {
    flex: 1;
    position: relative;
  }
</style>
