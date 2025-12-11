import request from '@/utils/http'

// 新增用户
export function fetchAddUser() {
  return request.post<any>({
    url: '/api/user/add',
    data: {
      username: 'string',
      password: 'string',
      nickname: 'string',
      email: 'string',
      phone: 'string',
      avatar: 'string'
    }
  })
}
