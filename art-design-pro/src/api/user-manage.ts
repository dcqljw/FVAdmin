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
