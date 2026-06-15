<!-- 角色管理页面 -->
<template>
  <div class="art-full-height">
    <ElCard class="art-table-card card-body-full" shadow="never">
      <div class="flex flex-row h-full">
        <div
          class="w-[280px] min-w-[280px] flex flex-col border-r border-[var(--el-border-color-lighter)] bg-[var(--el-bg-color)]"
        >
          <!-- 搜索和新增 -->
          <div class="flex items-center gap-2 p-3 border-b border-[var(--el-border-color-lighter)]">
            <ElInput
              v-model="roleSearchKeyword"
              placeholder="搜索名称/编码"
              clearable
              size="default"
              class="flex-1"
            >
              <template #prefix>
                <ElIcon><Search /></ElIcon>
              </template>
            </ElInput>
            <ElButton
              v-if="hasAuth('system:role:add')"
              type="primary"
              :icon="Plus"
              circle
              size="small"
              @click="showEditDialog('add')"
            />
          </div>

          <!-- 角色列表 -->
          <ElScrollbar class="flex-1 overflow-hidden scrollbar-view-py">
            <div
              v-for="role in filteredRoles"
              :key="role.id"
              class="role-item flex items-center justify-between px-3 py-2.5 cursor-pointer transition-all duration-200 rounded-md mx-1.5 hover:bg-[var(--el-fill-color-light)]"
              :class="{ 'role-item-active': isActive(role) }"
              @click="selectRole(role)"
            >
              <span
                class="text-sm truncate flex-1 mr-2 transition-colors"
                :class="
                  isActive(role)
                    ? 'text-[var(--el-color-primary)]'
                    : 'text-[var(--el-text-color-primary)]'
                "
              >
                {{ role.name }}
                <span
                  class="font-normal transition-colors"
                  :class="
                    isActive(role)
                      ? 'text-[var(--el-color-primary)]/70'
                      : 'text-[var(--el-text-color-secondary)]'
                  "
                  >({{ role.code }})</span
                >
              </span>
              <ElDropdown
                v-if="hasAuth('system:role:edit') || hasAuth('system:role:delete')"
                trigger="click"
                @command="(cmd: string) => handleRoleCommand(cmd, role)"
              >
                <ElIcon
                  class="role-more text-[var(--el-text-color-placeholder)] flex-shrink-0 opacity-0 transition-opacity duration-200 group-hover:opacity-100"
                  ><MoreFilled
                /></ElIcon>
                <template #dropdown>
                  <ElDropdownMenu>
                    <ElDropdownItem v-if="hasAuth('system:role:edit')" command="edit"
                      >编辑角色</ElDropdownItem
                    >
                    <ElDropdownItem v-if="hasAuth('system:role:delete')" command="delete" divided
                      >删除角色</ElDropdownItem
                    >
                  </ElDropdownMenu>
                </template>
              </ElDropdown>
            </div>
            <ElEmpty v-if="filteredRoles.length === 0" description="暂无角色" :image-size="60" />
          </ElScrollbar>
        </div>

        <!-- 右侧内容区域 -->
        <div class="flex-1 pl-4">
          <template v-if="currentRole">
            <RolePermissionPanel :role-data="currentRole" />
          </template>
          <div v-else class="flex items-center justify-center h-full">
            <ElEmpty description="请从左侧选择一个角色" :image-size="120" />
          </div>
        </div>

        <!-- 角色编辑弹窗 -->
        <RoleEditDialog
          v-model="dialogVisible"
          :dialog-type="dialogType"
          :role-data="editRoleData"
          @success="handleEditSuccess"
        />
      </div>
    </ElCard>
  </div>
</template>

<script setup lang="ts">
  import { Search, Plus, MoreFilled } from '@element-plus/icons-vue'
  import { fetchGetRoleList, fetchDeleteRole } from '@/api/system-manage'
  import RolePermissionPanel from './modules/role-permission-panel.vue'
  import RoleEditDialog from './modules/role-edit-dialog.vue'
  import { ElMessageBox } from 'element-plus'
  import { useAuth } from '@/hooks'

  defineOptions({ name: 'Role' })

  type RoleListItem = Api.SystemManage.RoleListItem

  const { hasAuth } = useAuth()

  const roleSearchKeyword = ref('')
  const roleList = ref<RoleListItem[]>([])
  const currentRole = ref<RoleListItem | undefined>(undefined)
  const dialogVisible = ref(false)
  const dialogType = ref<'add' | 'edit'>('add')
  const editRoleData = ref<RoleListItem | undefined>(undefined)

  /**
   * 加载全部角色列表
   */
  const loadRoles = async () => {
    try {
      const res = await fetchGetRoleList({ current: 1, size: 1000 })
      roleList.value = res.records
      // 默认选中第一个角色
      if (!currentRole.value && roleList.value.length > 0) {
        currentRole.value = roleList.value[0]
      }
    } catch (error) {
      console.error('加载角色列表失败:', error)
    }
  }

  /**
   * 根据搜索关键词过滤角色
   */
  const filteredRoles = computed(() => {
    const keyword = roleSearchKeyword.value.trim().toLowerCase()
    if (!keyword) return roleList.value
    return roleList.value.filter(
      (role) =>
        role.name.toLowerCase().includes(keyword) || role.code.toLowerCase().includes(keyword)
    )
  })

  /**
   * 选择角色
   */
  const selectRole = (role: RoleListItem) => {
    currentRole.value = role
  }

  /**
   * 当前角色是否为选中态
   */
  const isActive = (role: RoleListItem) => currentRole.value?.id === role.id

  /**
   * 显示编辑弹窗
   */
  const showEditDialog = (type: 'add' | 'edit', role?: RoleListItem) => {
    dialogType.value = type
    editRoleData.value = role
    dialogVisible.value = true
  }

  /**
   * 角色更多菜单操作
   */
  const handleRoleCommand = (command: string, role: RoleListItem) => {
    switch (command) {
      case 'edit':
        showEditDialog('edit', role)
        break
      case 'delete':
        handleDeleteRole(role)
        break
    }
  }

  /**
   * 删除角色
   */
  const handleDeleteRole = (role: RoleListItem) => {
    ElMessageBox.confirm(`确定删除角色"${role.name}"吗？此操作不可恢复！`, '删除确认', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
      .then(async () => {
        const res = await fetchDeleteRole(role.id)
        ElMessage.success(res.msg || '删除成功')
        // 本地移除已删除的角色，避免再发一次列表请求
        roleList.value = roleList.value.filter((r) => r.id !== role.id)
        if (currentRole.value?.id === role.id) {
          currentRole.value = roleList.value[0]
        }
      })
      .catch(() => {
        ElMessage.info('已取消删除')
      })
  }

  /**
   * 编辑成功后刷新列表
   */
  const handleEditSuccess = () => {
    loadRoles()
  }

  onMounted(() => {
    loadRoles()
  })
</script>

<style scoped>
  /* ElScrollbar 内部视图间距 */
  .scrollbar-view-py :deep(.el-scrollbar__view) {
    padding: 4px 0;
  }

  /* 角色项 hover 时显示更多按钮 */
  .role-item:hover .role-more {
    opacity: 1;
  }

  /* 角色项选中态 */
  .role-item-active {
    background-color: #165dff1a;
    font-weight: bold;
  }

  /* ElCard body 撑满 */
  .card-body-full :deep(.el-card__body) {
    height: 100%;
    padding: 16px 20px;
    overflow: auto;
    display: flex;
    flex-direction: column;
  }
</style>
