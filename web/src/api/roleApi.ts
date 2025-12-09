import axiosInstance from "@/utils/request.ts";

export function getRoleList() {
    return axiosInstance.post('/role')
}