import axios from "axios";
import type {AxiosRequestConfig, AxiosResponse, InternalAxiosRequestConfig} from 'axios'

const axiosInstance = axios.create({
    baseURL: "http://127.0.0.1:8000",
    timeout: 5000
});

axiosInstance.interceptors.request.use(
    (request: InternalAxiosRequestConfig) => {
        return request
    },
    (error) => {
        return Promise.reject(error)
    }
)

axiosInstance.interceptors.response.use(
    (response: AxiosResponse) => {
        return response
    }
)


export default axiosInstance