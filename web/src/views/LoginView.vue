<script setup lang="ts">
import {ref} from "vue";
import {Lock, User} from "@element-plus/icons-vue";

const username = ref();
const password = ref();

</script>

<template>
  <div class="flex justify-center h-100vh items-center bg-[#fafbfc] flex-col">
    <div class="flex flex-col gap-6 items-center w-[300px]">
      <div class="font-bold text-[30px]">FVAdmin</div>
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
      <el-button size="large" type="primary" class="w-full" @click="$router.push('/dashboard')">登录</el-button>
    </div>
    <div class="m-t[140px]">
      &copy;FVAdmin
    </div>
  </div>

</template>

<style scoped>

</style>