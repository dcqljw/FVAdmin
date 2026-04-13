import request from '@/utils/http'
import { AppRouteRecord } from '@/types/router'

// 获取用户列表
export function fetchGetUserList(params: Api.SystemManage.UserSearchParams) {
  return request.get<Api.SystemManage.UserList>({
    url: '/api/user/list',
    params
  })
}

// 获取角色列表
export function fetchGetRoleList(params: Api.SystemManage.RoleSearchParams) {
  return request.get<Api.SystemManage.RoleList>({
    url: '/api/role/list',
    params
  })
}

// 获取菜单列表
export function fetchGetMenuList() {
  return request.get<AppRouteRecord[]>({
    url: '/api/menu/list'
  })
}
// 根据角色获取菜单
export function fetchGetMenuByRole(roleId: number) {
  return request.get<string[]>({
    url: '/api/menu/get_checked',
    params: {
      role_id: roleId
    }
  })
}

// 根据角色设置菜单
export function fetchSetMenuByRole(roleId: number | undefined, menuIds: number[]) {
  return request.post<any>({
    url: '/api/menu/add_menu_permission',
    data: {
      role_id: roleId,
      menu_ids: menuIds
    }
  })
}

// 新增用户
export function fetchAddUser(formData: any) {
  return request.post<any>({
    url: '/api/user/add',
    data: {
      ...formData
    }
  })
}
// 修改用户
export function fetchUpdateUser(formData: any) {
  return request.post<any>({
    url: '/api/user/edit',
    data: {
      ...formData
    }
  })
}
// 删除用户
export function fetchDeleteUser(id: number) {
  return request.post<any>({
    url: `/api/user/delete?user_id=${id}`
  })
}
// 重置密码
export function fetchResetPassword(id: number) {
  return request.post<any>({
    url: `/api/user/reset-password?user_id=${id}`
  })
}
// 新增角色
export function fetchAddRole(formData: any) {
  return request.post<any>({
    url: '/api/role/add',
    data: {
      ...formData
    }
  })
}
// 删除角色
export function fetchDeleteRole(id: number) {
  return request.post<any>({
    url: `/api/role/delete?role_id=${id}`
  })
}
// 编辑角色
export function fetchEditRole(formData: any) {
  return request.post<any>({
    url: '/api/role/edit',
    data: {
      ...formData
    }
  })
}
// 添加菜单
export function fetchAddMenu(formData: any) {
  return request.post<any>({
    url: '/api/menu/add',
    data: {
      ...formData
    }
  })
}
export function fetchEditMenu(formData: any) {
  return request.post<any>({
    url: '/api/menu/edit',
    data: {
      ...formData
    }
  })
}
// 删除菜单
export function fetchDeleteMenu(id: number) {
  return request.post<any>({
    url: `/api/menu/delete?menu_id=${id}`
  })
}

export function fetchAiEdit(formData: any) {
  return request.post<any>({
    url: `/api/ai/add`,
    data: {
      ...formData
    }
  })
}
