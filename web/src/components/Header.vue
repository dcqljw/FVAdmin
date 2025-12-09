<script setup lang="ts">
import {useRouter} from "vue-router";
import {Icon} from '@iconify/vue'
import {useMenuStore} from "@/stores/menu.ts";
import {useUserStore} from "@/stores/user.ts";

const router = useRouter()
const menuStore = useMenuStore()
const userStore = useUserStore()

const logOut = () => {
  userStore.logOut()
  menuStore.clearMenuList()
  router.push('/login')
}

const closeWorkTab = (tab: any) => {
  menuStore.removeWorkTab(tab)
  console.log(menuStore.workTabList[menuStore.workTabList.length - 1].menu)
  router.push('/')
}

</script>

<template>
  <div class=" h-full">
    <div class="bg-[#ffffff] flex justify-between items-center flex-row h-[60px]">
      <div class="ml-2 flex items-center">
        <el-button text class="!p-1" @click="menuStore.setIsCollapse(!menuStore.isCollapse)">
          <Icon icon="mynaui:text-align-left" width="30" height="30"/>
        </el-button>
        <span class="text-sm">{{ $route.meta.title }}</span>
      </div>
      <div class="mr-6 flex gap-2">
        <el-button text class="!p-1 !m0">
          <Icon icon="mynaui:cog-two" width="24" height="24"/>
        </el-button>
        <el-button text class="!p-1 !m0">
          <Icon icon="mynaui:moon" width="24" height="24"/>
        </el-button>
        <el-popover
            :width="300"
            placement="bottom-end"
        >
          <template #reference>
            <el-avatar :size="30" src="https://cube.elemecdn.com/9/c2/f0ee8a3c7c9638a54940382568c9dpng.png"
                       class="cursor-pointer"/>
          </template>
          <div>
            <div class="flex items-center gap-2">
              <div class="flex">
                <el-avatar :size="40" src="https://cube.elemecdn.com/9/c2/f0ee8a3c7c9638a54940382568c9dpng.png"/>
              </div>
              <div class="flex flex-col ">
                <div>{{ userStore.userInfo?.nickname }}</div>
                <div class="text-[10px]">{{ userStore.userInfo?.email }}</div>
              </div>
            </div>
            <el-divider/>
            <div class="user-popover">
              <el-button text class="w-full" @click="$router.push('/user_info')">
                <Icon icon="mynaui:user" width="18" height="18" class="mr-2"/>
                <p>个人中心</p>
              </el-button>

            </div>
            <el-divider/>
            <el-button class="w-full" @click="logOut">退出登录</el-button>
          </div>
        </el-popover>
      </div>
    </div>
    <div v-if="false" class="h-[40px] flex items-center">
      <el-check-tag :checked="$route.path === item.menu" @click="$router.push(item.menu)" class="ml-2 mr-2"
                    v-for="item in menuStore.workTabList">
        <template #default>
          <div class="flex items-center gap-2">
            <Icon :icon="item.meta.icon" width="18" height="18"/>
            <span>{{ item.meta.title }}</span>
            <Icon icon="ri:close-fill" width="18" height="18" @click="closeWorkTab(item)"/>
          </div>
        </template>
      </el-check-tag>
    </div>
  </div>
</template>

<style scoped>
.user-popover .el-button {
  display: flex;
  justify-content: flex-start;
}
</style>