<!-- 角色权限面板 -->
<template>
  <ElTabs v-model="activeTab" class="h-full flex flex-col tabs-deep">
    <ElTabPane label="功能权限" name="permission">
      <ArtTableHeader
        @refresh="handleRefresh"
        layout="search,refresh,size,settings"
        :show-header-background="true"
        :show-border="true"
      >
        <template #left>
          <ElSpace wrap>
            <ElButton type="primary" @click="handleSave" v-ripple>保存权限</ElButton>
          </ElSpace>
        </template>
      </ArtTableHeader>
      <ArtTable
        :loading="tableLoading"
        :data="menuList"
        row-key="id"
        :tree-props="{ children: 'children' }"
        :default-expand-all="true"
        :show-pagination="false"
        :show-table-header="false"
      >
        <!-- 菜单列：自绘复选框，避免 ElTable 树形选择的坑 -->
        <ElTableColumn min-width="140">
          <template #header>
            <ElCheckbox
              :model-value="isAllChecked"
              :indeterminate="isAllIndeterminate"
              @change="handleSelectAll"
            >
              菜单
            </ElCheckbox>
          </template>
          <template #default="{ row }">
            <ElCheckbox
              :model-value="isMenuChecked(row.id)"
              :indeterminate="isMenuIndeterminate(row)"
              @change="(val: boolean | string | number) => onMenuCheck(row, !!val)"
            >
              <span class="menu-label">{{ row.title }}</span>
            </ElCheckbox>
          </template>
        </ElTableColumn>

        <!-- 权限列：按钮级权限复选框组 -->
        <ElTableColumn label="权限" min-width="480">
          <template #default="{ row }">
            <div v-if="row.authList?.length" class="auth-list">
              <ElCheckbox
                v-for="auth in row.authList"
                :key="auth.id"
                :model-value="isAuthChecked(auth.id)"
                @change="(val: boolean | string | number) => onAuthCheck(row, auth, !!val)"
              >
                {{ auth.title }}
              </ElCheckbox>
            </div>
            <span v-else class="text-[var(--el-text-color-placeholder)] text-xs">-</span>
          </template>
        </ElTableColumn>
      </ArtTable>
      <!-- 树形表格 -->
    </ElTabPane>

    <ElTabPane label="角色用户" name="users">
      <div v-if="activeTab === 'users'" class="role-users-tab">
        <ArtSearchBar
          v-model="userSearch"
          :items="userSearchItems"
          :label-width="'60px'"
          :show-expand="false"
          class="flex-shrink-0"
          @search="handleUserSearch"
          @reset="handleUserReset"
        />
        <ArtTable
          :loading="usersLoading"
          :data="usersData"
          :columns="usersColumns"
          :pagination="usersPagination"
          :show-table-header="false"
          class="flex-1 min-h-0"
          @pagination:size-change="handleUserSizeChange"
          @pagination:current-change="handleUserCurrentChange"
        />
      </div>
    </ElTabPane>
  </ElTabs>
</template>

<script setup lang="ts">
  import ArtTable from '@/components/core/tables/art-table/index.vue'
  import ArtSearchBar from '@/components/core/forms/art-search-bar/index.vue'
  import ArtAvatar from '@/components/core/base/art-avatar/index.vue'
  import { formatMenuTitle } from '@/utils/router'
  import { formatUserStatusTag } from '@/utils/formatters'
  import { useTable } from '@/hooks/core/useTable'
  import {
    fetchGetMenuList,
    fetchGetMenuByRole,
    fetchSetMenuByRole,
    fetchGetUserListByRole
  } from '@/api/system-manage'
  import type { AppRouteRecord } from '@/types/router'

  defineOptions({ name: 'RolePermissionPanel' })

  interface Props {
    roleData?: Api.SystemManage.RoleListItem
  }

  const props = defineProps<Props>()

  // ============ 表格行类型（由 AppRouteRecord 映射而来） ============

  interface AuthItem {
    id: number
    authMark: string
    title: string
  }

  interface MenuItem {
    id: number
    title: string
    children?: MenuItem[]
    authList?: AuthItem[]
  }

  // ============ 状态（单一数据源） ============

  // 用 ref<Set> 作为唯一数据源。由于 Set.add/delete 是原地突变不会改变 ref.value 引用，
  // 必须通过「构造新 Set 再赋值」的方式让 Vue 检测到变化、触发模板重渲染。
  // 所有对 Set 的修改必须经过下面的 helper，确保响应式生效。
  const menuList = ref<MenuItem[]>([])
  const tableLoading = ref(false)
  const checkedMenuIds = ref(new Set<number>())
  const checkedAuthIds = ref(new Set<number>())
  const activeTab = ref('permission')
  const userSearch = ref({ username: '', phone: '', email: '' })

  // ArtSearchBar 表单配置：用户名 / 手机号 / 邮箱
  const userSearchItems = [
    {
      key: 'username',
      label: '用户名',
      type: 'input',
      placeholder: '请输入用户名',
      props: { clearable: true }
    },
    {
      key: 'phone',
      label: '手机号',
      type: 'input',
      placeholder: '请输入手机号',
      props: { maxlength: 11, clearable: true }
    },
    {
      key: 'email',
      label: '邮箱',
      type: 'input',
      placeholder: '请输入邮箱',
      props: { clearable: true }
    }
  ]

  // 泛型 Set 操作 helper：因 Set.add/delete 是原地突变，需「构造新 Set 再赋值」触发 Vue 响应式
  const check = (set: Ref<Set<number>>, id: number) => {
    set.value = new Set(set.value).add(id)
  }
  const uncheck = (set: Ref<Set<number>>, id: number) => {
    const s = new Set(set.value)
    s.delete(id)
    set.value = s
  }
  const clearSet = (set: Ref<Set<number>>) => {
    set.value = new Set()
  }

  // ============ 数据加载与映射 ============

  // 把后端 AppRouteRecord[] 映射为组件内部 MenuItem[]。
  // 仅保留树形表格需要的字段：id / title / children / authList。
  const mapApiToMenu = (nodes: AppRouteRecord[]): MenuItem[] => {
    return nodes
      .filter((n) => n.id != null)
      .map((n) => {
        const item: MenuItem = {
          id: n.id as number,
          title: formatMenuTitle(n.meta?.title || '') || (n.name as string) || ''
        }
        if (n.meta?.authList?.length) {
          item.authList = n.meta.authList.map((a) => ({
            id: a.id,
            authMark: a.authMark,
            title: a.title
          }))
        }
        if (n.children?.length) {
          const mapped = mapApiToMenu(n.children as AppRouteRecord[])
          if (mapped.length) item.children = mapped
        }
        return item
      })
  }

  const loadMenuList = async () => {
    tableLoading.value = true
    try {
      const data = await fetchGetMenuList()
      menuList.value = mapApiToMenu(data ?? [])
    } catch (error) {
      console.error('[role-permission] 加载菜单树失败:', error)
      menuList.value = []
    } finally {
      tableLoading.value = false
    }
  }

  // ============ 查询：是否勾选（模板中调用，自动被依赖收集） ============

  const isMenuChecked = (id: number) => checkedMenuIds.value.has(id)
  const isAuthChecked = (id: number) => checkedAuthIds.value.has(id)

  // 半选状态：当前菜单未勾选、但其后代中存在至少一个已勾选。
  // 用 computed 返回 Set，依赖 checkedMenuIds.value 的变化自动重算。
  const indeterminateMenuIds = computed<Set<number>>(() => {
    const result = new Set<number>()
    const walk = (nodes: MenuItem[]) => {
      nodes.forEach((node) => {
        if (node.children?.length) {
          const descs = getDescendants(node)
          const someChecked = descs.some((d) => checkedMenuIds.value.has(d.id))
          const allChecked = descs.every((d) => checkedMenuIds.value.has(d.id))
          if (someChecked && !allChecked) result.add(node.id)
          walk(node.children)
        }
      })
    }
    walk(menuList.value)
    return result
  })

  const isMenuIndeterminate = (row: MenuItem) => indeterminateMenuIds.value.has(row.id)

  // ============ 全选状态 ============

  // 所有菜单节点（扁平化）
  const allMenuIds = computed<number[]>(() => {
    const ids: number[] = []
    const walk = (nodes: MenuItem[]) => {
      nodes.forEach((n) => {
        ids.push(n.id)
        if (n.children?.length) walk(n.children)
      })
    }
    walk(menuList.value)
    return ids
  })

  // 所有权限节点
  const allAuthIds = computed<number[]>(() => {
    const ids: number[] = []
    const walk = (nodes: MenuItem[]) => {
      nodes.forEach((n) => {
        n.authList?.forEach((a) => ids.push(a.id))
        if (n.children?.length) walk(n.children)
      })
    }
    walk(menuList.value)
    return ids
  })

  const isAllChecked = computed(() => {
    const total = allMenuIds.value.length + allAuthIds.value.length
    if (total === 0) return false
    return checkedMenuIds.value.size + checkedAuthIds.value.size === total
  })

  const isAllIndeterminate = computed(() => {
    const checked = checkedMenuIds.value.size + checkedAuthIds.value.size
    const total = allMenuIds.value.length + allAuthIds.value.length
    return checked > 0 && checked < total
  })

  const handleSelectAll = (val: boolean | string | number) => {
    if (val) {
      // 全选：勾选所有菜单 + 所有权限
      const newMenuIds = new Set(allMenuIds.value)
      const newAuthIds = new Set(allAuthIds.value)
      checkedMenuIds.value = newMenuIds
      checkedAuthIds.value = newAuthIds
    } else {
      // 全不选
      clearSet(checkedMenuIds)
      clearSet(checkedAuthIds)
    }
  }

  // ============ 树遍历工具 ============

  // 获取所有后代（不含自身）
  const getDescendants = (node: MenuItem): MenuItem[] => {
    const result: MenuItem[] = []
    const walk = (n: MenuItem) => {
      n.children?.forEach((c) => {
        result.push(c)
        walk(c)
      })
    }
    walk(node)
    return result
  }

  // 获取从根到父节点的链（不含自身），用于"勾选权限时自动勾选祖先菜单"
  const getAncestors = (targetId: number): MenuItem[] => {
    const path: MenuItem[] = []
    const walk = (nodes: MenuItem[]): boolean => {
      for (const node of nodes) {
        if (node.id === targetId) return true
        path.push(node)
        if (node.children?.length && walk(node.children)) return true
        path.pop()
      }
      return false
    }
    walk(menuList.value)
    return path
  }

  // ============ 联动工具 ============

  // 对 row 及其所有后代统一执行勾选或取消（含各自的 authList）
  const cascadeSubtree = (row: MenuItem, checked: boolean) => {
    const mfn = (id: number) => (checked ? check(checkedMenuIds, id) : uncheck(checkedMenuIds, id))
    const afn = (id: number) => (checked ? check(checkedAuthIds, id) : uncheck(checkedAuthIds, id))
    ;[row, ...getDescendants(row)].forEach((node) => {
      mfn(node.id)
      node.authList?.forEach((a) => afn(a.id))
    })
  }

  // ============ 事件处理 ============

  const onMenuCheck = (row: MenuItem, checked: boolean) => {
    cascadeSubtree(row, checked)
  }

  const onAuthCheck = (row: MenuItem, auth: AuthItem, checked: boolean) => {
    if (checked) {
      check(checkedAuthIds, auth.id)
      check(checkedMenuIds, row.id)
      getAncestors(row.id).forEach((a) => check(checkedMenuIds, a.id))
    } else {
      uncheck(checkedAuthIds, auth.id)
      const anyAuthLeft = row.authList?.some((a) => checkedAuthIds.value.has(a.id)) ?? false
      if (!anyAuthLeft) {
        cascadeSubtree(row, false)
      }
    }
  }

  const handleRefresh = async () => {
    clearSet(checkedMenuIds)
    clearSet(checkedAuthIds)
    await loadMenuList()
    if (props.roleData?.id) {
      await loadRolePermissions(props.roleData.id)
    }
    ElMessage.success('已刷新')
  }

  const handleSave = async () => {
    if (!props.roleData?.id) {
      ElMessage.warning('请先选择角色')
      return
    }
    tableLoading.value = true
    try {
      // 后端把菜单 id 与权限 id 放在同一个 id 空间，合并后一起提交
      const merged = [...Array.from(checkedMenuIds.value), ...Array.from(checkedAuthIds.value)]
      await fetchSetMenuByRole(props.roleData.id, merged)
      ElMessage.success(
        `保存成功：菜单 ${checkedMenuIds.value.size} 项，权限 ${checkedAuthIds.value.size} 项`
      )
    } catch (error) {
      console.error('[role-permission] 保存失败:', error)
      ElMessage.error('保存失败')
    } finally {
      tableLoading.value = false
    }
  }

  // ============ 角色切换与回填 ============

  // 把后端返回的已勾选 id 列表（菜单 + 权限混合）同步到两个 Set。
  //
  // 后端说了哪些 id 就只勾哪些 id，不自作主张：
  //   - 菜单 id 命中 → 只勾该菜单自身，不碰 authList
  //   - 权限 id 命中 → 勾该权限 + 补勾自身菜单 + 所有祖先（保证在树上可见）
  const applyCheckedIds = (ids: number[]) => {
    const idSet = new Set(ids.map((id) => Number(id)))
    clearSet(checkedMenuIds)
    clearSet(checkedAuthIds)

    if (!idSet.size || !menuList.value.length) return

    const walk = (nodes: MenuItem[]) => {
      nodes.forEach((node) => {
        if (idSet.has(node.id)) {
          check(checkedMenuIds, node.id)
        }

        let authHit = false
        node.authList?.forEach((a) => {
          if (idSet.has(a.id)) {
            check(checkedAuthIds, a.id)
            authHit = true
          }
        })

        // 有权限命中 → 就地补勾自身菜单 + 所有祖先
        if (authHit) {
          check(checkedMenuIds, node.id)
          getAncestors(node.id).forEach((a) => check(checkedMenuIds, a.id))
        }

        if (node.children?.length) walk(node.children)
      })
    }
    walk(menuList.value)
  }

  const loadRolePermissions = async (roleId: number) => {
    tableLoading.value = true
    try {
      const checkedIds = await fetchGetMenuByRole(roleId)
      const rawIds = (checkedIds ?? []).map((id) => Number(id))
      applyCheckedIds(rawIds)
    } catch (error) {
      console.error('[role-permission] 加载角色权限失败:', error)
    } finally {
      tableLoading.value = false
    }
  }

  // ============ 角色用户列表 ============

  type UserListItem = Api.SystemManage.UserListItem

  // 把 roleId 闭包进 apiFn：每次请求都带当前 props.roleData.id
  // 给 params 显式标注类型，让 useTable 的 TApiFn 泛型能正确推断 TRecord=UserListItem
  const {
    data: usersData,
    loading: usersLoading,
    columns: usersColumns,
    pagination: usersPagination,
    searchParams: usersSearchParams,
    getData: getUsersByPage,
    handleSizeChange: handleUserSizeChange,
    handleCurrentChange: handleUserCurrentChange,
    resetSearchParams: resetUserSearchParams
  } = useTable({
    core: {
      apiFn: (params: Api.SystemManage.UserSearchParams) =>
        fetchGetUserListByRole(props.roleData!.id, params),
      apiParams: {
        current: 1,
        size: 10
      },
      // 避免在 props.roleData 还未就绪时拉取
      immediate: false,
      columnsFactory: () => [
        {
          prop: 'username',
          label: '用户',
          minWidth: 220,
          formatter: (row: UserListItem) =>
            h('div', { class: 'user flex-c' }, [
              h('div', { class: 'size-9.5 shrink-0' }, [
                h(ArtAvatar, { name: row.nickname || row.username, size: 38 })
              ]),
              h('div', { class: 'ml-2' }, [
                h('p', { class: 'user-name' }, row.nickname ? row.nickname : row.username),
                h('p', { class: 'email' }, row.email)
              ])
            ])
        },
        { prop: 'phone', label: '手机号', minWidth: 120 },
        {
          prop: 'status',
          label: '状态',
          width: 80,
          formatter: (row: UserListItem) => formatUserStatusTag(row.status)
        },
        { prop: 'created_at', label: '创建日期', minWidth: 160 }
      ]
    }
  })

  const handleUserSearch = async () => {
    // 把内联筛选条件合并进 useTable 的 searchParams，触发带分页重置的搜索
    Object.assign(usersSearchParams, {
      username: userSearch.value.username || undefined,
      phone: userSearch.value.phone || undefined,
      email: userSearch.value.email || undefined
    })
    await getUsersByPage()
  }

  const handleUserReset = async () => {
    // ArtSearchBar 内部已经会把 modelValue 全部置为 undefined；下游 handleUserSearch
    // 用 `|| undefined` 把空串与 undefined 视为一致，所以无需再写一次 userSearch。
    await resetUserSearchParams()
  }

  // 首次进入 / 切换角色：先保证菜单树已加载，再回填权限
  watch(
    () => props.roleData?.id,
    async (newId) => {
      clearSet(checkedMenuIds)
      clearSet(checkedAuthIds)
      if (!newId) return

      if (!menuList.value.length) {
        await loadMenuList()
      }
      await loadRolePermissions(newId)
      // 切换角色时重置筛选并刷新用户列表
      userSearch.value = { username: '', phone: '', email: '' }
      await resetUserSearchParams()
    },
    { immediate: true }
  )
</script>

<style scoped>
  .tabs-deep :deep(.el-tabs__header) {
    flex-shrink: 0;
  }

  .tabs-deep :deep(.el-tabs__content) {
    flex: 1;
    min-height: 0;
    display: flex;
    flex-direction: column;
  }

  .tabs-deep :deep(.el-tab-pane) {
    flex: 1;
    min-height: 0;
    display: flex;
    flex-direction: column;
  }

  /* 权限列复选框组：横向排列 + 自动换行 */
  .auth-list {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 4px 16px;
  }

  /* 菜单列复选框文字间距微调 */
  .menu-label {
    margin-left: 2px;
  }

  /* 补偿 ArtTable 全局 margin-top: 10px，防止底部溢出 */
  :deep(.art-table) {
    height: calc(100% - 86px) !important;
  }

  /* 角色用户 tab：搜索栏 + 表格用 flex 列布局，
     搜索栏高度不固定，避免硬编码像素偏移。
     覆盖上面那条全局 art-table 高度，让 flex 决定尺寸。 */
  .role-users-tab {
    height: calc(100% - 40px);
  }
</style>
