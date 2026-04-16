<script setup lang="ts">
  import { ref, onMounted } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import type { Node, Edge, Connection } from '@vue-flow/core'
  import { VueFlow, useVueFlow } from '@vue-flow/core'
  import { Controls } from '@vue-flow/controls'

  // 自定义节点组件
  import StartNode from './modules/StartNode.vue'
  import EndNode from './modules/EndNode.vue'
  import NumberInputNode from './modules/NumberInputNode.vue'
  import AddNode from './modules/AddNode.vue'
  import ResultNode from './modules/ResultNode.vue'
  import AddNodePanel from './modules/AddNodePanel.vue'

  const route = useRoute()
  const router = useRouter()
  const { project, addEdges, fitView } = useVueFlow()

  // 从路由参数获取工作流 id
  const flowId = ref((route.params.id as string) || 'default')

  // 模拟工作流数据（写死）
  const flowData: Record<string, { name: string; nodes: Node[]; edges: Edge[] }> = {
    default: {
      name: 'test',
      nodes: [
        {
          id: 'start-1',
          type: 'start',
          position: { x: 100, y: 200 },
          data: { label: '开始', inputVar: 'input', inputType: 'str' }
        },
        {
          id: 'end-1',
          type: 'end',
          position: { x: 500, y: 200 },
          data: { label: '结束', outputVar: 'output', outputType: 'str', returnType: '返回变量' }
        }
      ],
      edges: [
        {
          id: 'edge-start-end',
          source: 'start-1',
          target: 'end-1',
          sourceHandle: 'output',
          targetHandle: 'input'
        }
      ]
    }
  }

  // 节点数据
  const nodes = ref<Node[]>([])
  const flowName = ref('test')

  // 边数据
  const edges = ref<Edge[]>([])

  // 添加节点面板显示状态
  const addPanelVisible = ref(false)

  // 加载工作流数据
  function loadFlowData() {
    const data = flowData[flowId.value] || flowData.default
    flowName.value = data.name
    nodes.value = JSON.parse(JSON.stringify(data.nodes))
    edges.value = JSON.parse(JSON.stringify(data.edges))
  }

  onMounted(() => {
    loadFlowData()
  })

  // 生成唯一 id
  function generateId() {
    return `node-${Date.now()}-${Math.random().toString(36).slice(2, 6)}`
  }

  // 获取节点默认数据
  function getDefaultData(type: string) {
    switch (type) {
      case 'start':
        return { label: '开始', inputVar: 'input', inputType: 'str' }
      case 'end':
        return { label: '结束', outputVar: 'output', outputType: 'str', returnType: '返回变量' }
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

    const bounds = (event.target as HTMLElement).closest('.vue-flow')?.getBoundingClientRect()
    if (!bounds) return

    const x = event.clientX - bounds.left
    const y = event.clientY - bounds.top

    const position = project({ x, y })

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

  // 处理添加节点
  function handleAddNode(type: string) {
    // 计算画布中心位置
    const centerX = 400
    const centerY = 200

    const newNode: Node = {
      id: generateId(),
      type,
      position: { x: centerX, y: centerY },
      data: getDefaultData(type)
    }

    nodes.value = [...nodes.value, newNode]
  }
</script>

<template>
  <div class="flow-page">
    <!-- 顶部 Header -->
    <div class="flow-header">
      <div class="header-left">
        <span class="back-btn" @click="router.push('/flow/list')">&#8592;</span>
        <div class="flow-info">
          <span class="flow-name">{{ flowName }}</span>
          <span class="flow-status">
            <svg width="14" height="14" viewBox="0 0 16 16" fill="none">
              <circle cx="8" cy="8" r="6" fill="#22c55e" />
              <path
                d="M5.5 8L7 9.5L10.5 6"
                stroke="white"
                stroke-width="1.5"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
            </svg>
          </span>
          <span class="flow-status">
            <svg width="14" height="14" viewBox="0 0 16 16" fill="none">
              <circle cx="8" cy="8" r="6" fill="#22c55e" />
            </svg>
          </span>
        </div>
        <span class="save-info">已自动保存 20:38:34</span>
        <span class="unsaved-badge">有尚未发布的修改</span>
      </div>
      <div class="header-right">
        <button class="icon-btn" title="分享">
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
            <path
              d="M4 10H12M12 10L8 6M12 10L8 14"
              stroke="#666"
              stroke-width="1.5"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>
        </button>
        <button class="icon-btn" title="历史">
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
            <circle cx="8" cy="8" r="6" stroke="#666" stroke-width="1.5" />
            <path d="M8 5V8L10 9" stroke="#666" stroke-width="1.5" stroke-linecap="round" />
          </svg>
        </button>
        <button class="publish-btn">发布</button>
        <button class="icon-btn" title="更多">
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
            <circle cx="4" cy="8" r="1.5" fill="#666" />
            <circle cx="8" cy="8" r="1.5" fill="#666" />
            <circle cx="12" cy="8" r="1.5" fill="#666" />
          </svg>
        </button>
      </div>
    </div>

    <!-- 画布区域 -->
    <div class="flow-canvas">
      <VueFlow
        v-model:nodes="nodes"
        v-model:edges="edges"
        @connect="onConnect"
        @drop="onDrop"
        @dragover="onDragOver"
      >
        <Controls position="top-right" />

        <!-- 开始节点 -->
        <template #node-start="nodeProps">
          <StartNode v-bind="nodeProps" />
        </template>

        <!-- 结束节点 -->
        <template #node-end="nodeProps">
          <EndNode v-bind="nodeProps" />
        </template>

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

      <!-- 底部工具栏 -->
      <div class="bottom-toolbar">
        <div class="toolbar-group">
          <span class="zoom-label">77%</span>
        </div>
        <button class="add-node-btn" @click="addPanelVisible = true">
          <span>+ 添加节点</span>
        </button>
        <button class="run-btn">
          <span class="run-icon">&#9654;</span>
          <span>试运行</span>
        </button>
      </div>
    </div>

    <!-- 添加节点面板 -->
    <AddNodePanel v-model:visible="addPanelVisible" @add="handleAddNode" />
  </div>
</template>

<style>
  @import '@vue-flow/core/dist/style.css';
  @import '@vue-flow/core/dist/theme-default.css';
  @import '@vue-flow/controls/dist/style.css';
</style>

<style scoped>
  .flow-page {
    display: flex;
    flex-direction: column;
    height: calc(100vh - 110px);
    overflow: hidden;
    background: #f5f5f7;
  }

  /* 顶部 Header */
  .flow-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 52px;
    padding: 0 16px;
    background: #fff;
    border-bottom: 1px solid #e8e8ee;
    flex-shrink: 0;
  }

  .header-left {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .back-btn {
    font-size: 18px;
    color: #666;
    cursor: pointer;
    padding: 4px;
    border: none;
    background: none;
  }

  .flow-info {
    display: flex;
    align-items: center;
    gap: 4px;
  }

  .flow-name {
    font-size: 15px;
    font-weight: 600;
    color: #333;
  }

  .flow-status {
    display: flex;
    align-items: center;
  }

  .save-info {
    font-size: 12px;
    color: #999;
  }

  .unsaved-badge {
    font-size: 11px;
    color: #f59e0b;
    background: #fffbeb;
    padding: 2px 8px;
    border-radius: 10px;
  }

  .header-right {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .icon-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 32px;
    border: none;
    background: none;
    border-radius: 6px;
    cursor: pointer;
    transition: background 0.15s;
  }

  .icon-btn:hover {
    background: #f0f0f5;
  }

  .publish-btn {
    padding: 6px 16px;
    background: #6366f1;
    color: #fff;
    border: none;
    border-radius: 6px;
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
    transition: background 0.15s;
  }

  .publish-btn:hover {
    background: #4f46e5;
  }

  /* 画布区域 */
  .flow-canvas {
    flex: 1;
    position: relative;
    overflow: hidden;
  }

  /* 底部工具栏 */
  .bottom-toolbar {
    position: absolute;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 6px 8px;
    background: #fff;
    border: 1px solid #e0e0e8;
    border-radius: 10px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
    z-index: 10;
  }

  .toolbar-group {
    display: flex;
    align-items: center;
    padding: 0 8px;
  }

  .zoom-label {
    font-size: 12px;
    color: #666;
  }

  .add-node-btn {
    display: flex;
    align-items: center;
    gap: 4px;
    padding: 6px 14px;
    background: #f0f2ff;
    color: #6366f1;
    border: 1px solid #d0d4f0;
    border-radius: 6px;
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.15s;
  }

  .add-node-btn:hover {
    background: #e0e4ff;
    border-color: #6366f1;
  }

  .run-btn {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 6px 16px;
    background: #22c55e;
    color: #fff;
    border: none;
    border-radius: 6px;
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
    transition: background 0.15s;
  }

  .run-btn:hover {
    background: #16a34a;
  }

  .run-icon {
    font-size: 10px;
  }
</style>
