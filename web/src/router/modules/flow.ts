import { AppRouteRecord } from '@/types/router'

export const flowRoutes: AppRouteRecord = {
  name: 'Flow',
  path: '/flow',
  component: '/index/index',
  meta: {
    title: '工作流',
    icon: 'ri:flow-chart',
    roles: ['R_SUPER', 'R_ADMIN']
  },
  children: [
    {
      path: '',
      name: 'FlowList',
      component: '/flow/index',
      meta: {
        title: '工作流列表',
        keepAlive: true
      }
    },
    {
      path: 'editor/:id',
      name: 'FlowEditor',
      component: '/flow/editor/index',
      meta: {
        title: '工作流编辑',
        isHide: true,
        isHideTab: true
      }
    }
  ]
}
