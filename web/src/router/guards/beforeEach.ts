import type {NavigationGuardNext, RouteLocationNormalized, Router, RouteRecordRaw} from "vue-router";
import {getMenuList} from "@/api/userApi.ts";
import {useMenuStore} from "@/stores/menu.ts";
import {useUserStore} from "@/stores/user.ts";


let isAddDynamicRoute = false;

export function setupBeforeEachGuard(router: Router) {
    router.beforeEach(
        async (
            to: RouteLocationNormalized,
            from: RouteLocationNormalized,
            next: NavigationGuardNext
        ) => {
            await handleRouteGuard(to, from, next, router)
        }
    )
}

async function handleRouteGuard(
    to: RouteLocationNormalized,
    from: RouteLocationNormalized,
    next: NavigationGuardNext,
    router: Router
): Promise<void> {
    if (to.path === '/login') {
        next()
        return
    }
    if (isAddDynamicRoute) {
        next()
    } else {
        const menuStore = useMenuStore()
        const userStore = useUserStore();
        console.log(menuStore.menuList)
        if (menuStore.menuList.length > 0) {
            next()
        } else {
            if (userStore.token === '') {
                next('/login')
                return
            }
            let routes: any[] = []
            await getMenuList().then(res => {
                console.log(res)
                routes = res.data.data
            })
            menuStore.setMenuList(routes)
            await addDynamicRoutes(routes, 'Layout', router)
            isAddDynamicRoute = true
            console.log(router.getRoutes())
            next({...to, replace: true})
        }

    }

}

const addDynamicRoutes = async (routes: any[], parentName = 'Layout', router: Router) => {
    const allDynamicComponents = import.meta.glob("../../views/**/*.vue", {eager: false})
    routes.forEach(route => {
        const component = allDynamicComponents[`../../views/${route.component}.vue`]
        // 构造 Vue Router 格式的路由
        console.log(route)

        const vueRoute = {
            path: route.path,
            name: route.name,
            component: component,
            meta: route.meta,
            children: []
        }


        console.log(parentName, vueRoute)
        // 添加到父路由
        router.addRoute(parentName, vueRoute)
        // 递归添加子路由
        if (route.children && route.children.length > 0) {
            if (route.menu_type === 0) {
                parentName = 'Layout'
            } else {
                parentName = route.name!
            }
            addDynamicRoutes(route.children, route.name!, router)
        }
    })
}