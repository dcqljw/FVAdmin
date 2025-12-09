<script setup lang="ts">
import {ref} from "vue";
import {useMenuStore} from "@/stores/menu.ts";
import {Icon} from '@iconify/vue'

const menuStore = useMenuStore()
console.log(menuStore.menuList)
const test = ref(true)
const menuClickHandler = (item: any) => {
  menuStore.addWorkTab(item)
  console.log(item)
}

</script>

<template>
  <el-menu
      router
      :default-active="$route.path"
      :collapse="menuStore.isCollapse"
      :default-openeds="[$route.path]"
  >
    <template v-for="item in menuStore.menuList">
      <el-sub-menu v-if="item.children.length > 0" :index="item.menu">
        <template #title>
          <div class="flex mr-2">
            <Icon :icon="item.meta.icon" width="24" height="24"/>
          </div>
          <span>{{ item.meta.title }}</span>
        </template>
        <template v-for="child in item.children">
          <el-menu-item :index="child.menu" @click="menuClickHandler(child)">
            <div class="flex mr-2">
              <Icon :icon="child.meta.icon" width="24" height="24"/>
            </div>
            <span slot="title">{{ child.meta.title }}</span>
          </el-menu-item>
        </template>
      </el-sub-menu>
      <el-menu-item v-else :index="item.menu" @click="menuClickHandler(item)">
        <div class="flex mr-2">
          <Icon :icon="item.meta.icon" width="24" height="24"/>
        </div>
        <span slot="title">{{ item.meta.title }}</span>
      </el-menu-item>
    </template>
  </el-menu>
</template>

<style scoped>

</style>