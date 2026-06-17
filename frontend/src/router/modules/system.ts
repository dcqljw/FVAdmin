import { AppRouteRecord } from '@/types/router'

export const systemRoutes: AppRouteRecord = {
  path: '/system',
  name: 'System',
  component: '/index/index',
  meta: {
    title: 'menus.system.title',
    icon: 'ri:user-3-line',
    roles: ['R_SUPER', 'R_ADMIN']
  },
  children: [
    {
      path: 'user',
      name: 'User',
      component: '/system/user',
      meta: {
        title: 'menus.system.user',
        keepAlive: true,
        roles: ['R_SUPER', 'R_ADMIN'],
        authList: [
          { id: 4, title: '新增用户', authMark: 'system:user:add' },
          { id: 5, title: '编辑用户', authMark: 'system:user:edit' },
          { id: 6, title: '删除用户', authMark: 'system:user:delete' },
          { id: 7, title: '重置密码', authMark: 'system:user:reset-password' }
        ]
      }
    },
    {
      path: 'role',
      name: 'Role',
      component: '/system/role',
      meta: {
        title: 'menus.system.role',
        keepAlive: true,
        roles: ['R_SUPER'],
        authList: [
          { id: 8, title: '新增角色', authMark: 'system:role:add' },
          { id: 9, title: '编辑角色', authMark: 'system:role:edit' },
          { id: 10, title: '删除角色', authMark: 'system:role:delete' }
        ]
      }
    },
    {
      path: 'user-center',
      name: 'UserCenter',
      component: '/system/user-center',
      meta: {
        title: 'menus.system.userCenter',
        isHide: true,
        keepAlive: true,
        isHideTab: true
      }
    },
    {
      path: 'menu',
      name: 'Menus',
      component: '/system/menu',
      meta: {
        title: 'menus.system.menu',
        keepAlive: true,
        roles: ['R_SUPER'],
        authList: [
          { id: 1, title: '新增', authMark: 'system:menu:add' },
          { id: 2, title: '编辑', authMark: 'system:menu:edit' },
          { id: 3, title: '删除', authMark: 'system:menu:delete' }
        ]
      }
    },
    {
      path: 'operation-log',
      name: 'OperationLog',
      component: '/system/operation-log',
      meta: {
        title: 'menus.system.operationLog',
        keepAlive: true,
        roles: ['R_SUPER', 'R_ADMIN']
      }
    }
  ]
}
