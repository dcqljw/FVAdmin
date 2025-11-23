import {defineStore} from "pinia";
import {ref} from "vue";

interface menuList {
    name: string,
    path: string,
    menu: string,
    component: string,
    children?: menuList[],
    meta: {
        title: string,
        icon: string
    },
}

export const useMenuStore = defineStore("menuStore", () => {
    const menuList = ref<menuList[]>([])
    const isCollapse = ref<boolean>(false)
    const setMenuList = (list: any) => {
        menuList.value = list
    }
    const setIsCollapse = (newIsCollapse: boolean) => {
        isCollapse.value = newIsCollapse
    }

    return {
        menuList,
        isCollapse,
        setMenuList,
        setIsCollapse
    }
})