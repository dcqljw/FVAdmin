import {defineStore} from "pinia";
import {ref} from "vue";

interface menuList {
    name: string,
    path: string,
    menu: string,
    component: string,
    children: menuList[],
    meta: {
        title: string,
        icon: string
    },
}

export const useMenuStore = defineStore("menuStore", () => {
    const menuList = ref<menuList[]>([])
    const currentWorkTab = ref({})
    const workTabList = ref<any[]>([])
    const isCollapse = ref<boolean>(false)
    const setMenuList = (list: any) => {
        menuList.value = list
    }
    const setIsCollapse = (newIsCollapse: boolean) => {
        isCollapse.value = newIsCollapse
    }

    const setCurrentWorkTab = (menu: any) => {
        currentWorkTab.value = menu
    }
    const setWorkTabList = (list: any) => {
        workTabList.value = list
    }
    const addWorkTab = (menu: any) => {
        if (!workTabList.value.includes(menu)) {
            workTabList.value.push(menu)
        }
    }

    const removeWorkTab = (menu: any) => {
        workTabList.value = workTabList.value.filter((item: any) => item.path !== menu.path)
    }

    const clearMenuList = () => {
        menuList.value = []
    }

    return {
        menuList,
        isCollapse,
        currentWorkTab,
        workTabList,
        setMenuList,
        setIsCollapse,
        setCurrentWorkTab,
        setWorkTabList,
        addWorkTab,
        removeWorkTab,
        clearMenuList
    }
})