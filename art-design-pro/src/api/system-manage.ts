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
