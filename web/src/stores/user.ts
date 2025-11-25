import {defineStore} from "pinia";
import {ref} from "vue";

interface UserInfo {
    username: string,
    nickname: string,
    avatar: string,
    roles: string[]
    permissions: string[]
    email: string
    phone: string
}

export const useUserStore = defineStore("userStore", () => {
    const userInfo = ref<UserInfo>()
    const token = ref<string>("")

    const setToken = (newToken: string) => {
        token.value = newToken
    }
    return {
        userInfo,
        token,
        setToken,
    }
}, {
    persist: true
})