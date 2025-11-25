import axiosInstance from '@/utils/request.ts'


export function LoginApi(username: string, password: string) {
    return axiosInstance.post('/auth/login', {
        username: username,
        password: password
    })
}

export function userInfoApi() {
    return axiosInstance.post('/user/user_info')
}

export function getMenuList() {
    return axiosInstance.get('/menu/menu_list')
}