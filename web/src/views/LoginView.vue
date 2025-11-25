<script setup lang="ts">
import {ref} from "vue";
import {useRouter} from "vue-router";
import {ElMessage} from "element-plus";
import {Lock, User} from "@element-plus/icons-vue";

import {LoginApi, userInfoApi} from "@/api/userApi.ts";
import {useUserStore} from "@/stores/user.ts";
import {Icon} from "@iconify/vue";

const router = useRouter();
const userStore = useUserStore();


const username = ref();
const password = ref();

const login = () => {
  LoginApi(username.value, password.value).then(res => {
    console.log(res)
    if (res.data.code === 200) {
      userStore.setToken(res.data.data)
      userInfoApi().then(res => {
        console.log(res)
        userStore.userInfo = res.data.data
      })
      router.push("/")
    } else {
      ElMessage({
        message: res.data.message,
        type: "error",
      })
    }
  })
}

</script>

<template>
  <div class="flex justify-center h-100vh items-center bg-[#fafbfc] flex-col">
    <div class="flex flex-col gap-6 items-center w-[300px]">

      <div class="flex items-center gap-2">
        <Icon icon="skill-icons:fastapi" width="30" height="30"/>
        <span class="font-bold text-[30px]">
          FVAdmin
        </span>
      </div>
      <el-input
          v-model="username"
          :prefix-icon="User"
          size="large"
          placeholder="账号"/>
      <el-input
          v-model="password"
          :prefix-icon="Lock"
          size="large"
          placeholder="密码"
          show-password/>
      <el-button size="large" type="primary" class="w-full" @click="login">登录</el-button>
    </div>
    <div class="m-t[140px]">
      &copy;FVAdmin
    </div>
  </div>

</template>

<style scoped>

</style>