<script setup lang="ts">
import {Icon} from "@iconify/vue";
import {useMenuStore} from "@/stores/menu.ts";

import Header from "@/components/Header.vue";
import Menu from "@/components/Menu.vue";

const menuStore = useMenuStore();
</script>

<template>
  <div class="common-layout">
    <el-container class="h-100vh">
      <el-aside :class="menuStore.isCollapse ? '!w-auto' : '!w-[200px]'">
          <div class="bg-[#ffffff] h-full b-r-solid b-r-1 b-r-[#00000014]">
            <div class="h-15 flex items-center justify-center gap-3">
              <Icon icon="skill-icons:fastapi" width="30" height="30"/>
              <p v-if="!menuStore.isCollapse" class="font-bold text-[20px]">FVAdmin</p>
            </div>
            <Menu/>
          </div>
      </el-aside>
      <el-container>
        <el-header class="!p-0  ">
          <Header/>
        </el-header>
        <el-main>
          <RouterView/>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<style scoped>
.common-layout {
  background: #fafbfc;
}
</style>