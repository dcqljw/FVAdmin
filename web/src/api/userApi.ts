import axiosInstance from '@/utils/request.ts'


export function getMenuList() {
    return axiosInstance.get('/menu')
}