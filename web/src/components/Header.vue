<script setup lang="ts">
import {ref} from 'vue';
import {Icon} from '@iconify/vue'
import {useMenuStore} from "@/stores/menu.ts";

const menuStore = useMenuStore()

</script>

<template>
  <div class="bg-[#ffffff] h-full flex justify-between items-center">
    <div class="ml-2">
      <el-button text class="!p-1" @click="menuStore.setIsCollapse(!menuStore.isCollapse)">
        <Icon icon="mynaui:text-align-left" width="30" height="30"/>
      </el-button>
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
          trigger="click"
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
              <div>Admin</div>
              <div class="text-[10px]">dcq0516@gmail.com</div>
            </div>
          </div>
          <el-divider/>
          <div class="user-popover">
            <el-button text class="w-full">
              <Icon icon="mynaui:user" width="18" height="18" class="mr-2"/>
              <p>个人中心</p>
            </el-button>

          </div>
          <el-divider/>
          <el-button class="w-full">退出登录</el-button>
        </div>
      </el-popover>
    </div>
  </div>
</template>

<style scoped>
.user-popover .el-button {
  display: flex;
  justify-content: flex-start;
}
</style>