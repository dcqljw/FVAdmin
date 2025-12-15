import request from '@/utils/http'

// 新增用户
export function fetchAddUser(fromData: any) {
  return request.post<any>({
    url: '/api/user/add',
    data: {
      ...fromData
    }
  })
}
// 修改用户
export function fetchUpdateUser(fromData: any) {
  return request.post<any>({
    url: '/api/user/edit',
    data: {
      ...fromData
    }
  })
}
// 删除用户
export function fetchDeleteUser(id: number) {
  return request.post<any>({
    url: `/api/user/delete?user_id=${id}`
  })
}
