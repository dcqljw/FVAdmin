import type {NavigationGuardNext, RouteLocationNormalized, Router, RouteRecordRaw} from "vue-router";
import {getMenuList} from "@/api/userApi.ts";
import {useMenuStore} from "@/stores/menu.ts";


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
    if (isAddDynamicRoute) {
        next()
    } else {
        const menuStore = useMenuStore()
        console.log(menuStore.menuList)
        if (menuStore.menuList.length > 0) {
            next()
        } else {
            let routes: any[] = []
            await getMenuList().then(res => {
                console.log(res)
                routes = res.data
            })
            menuStore.setMenuList(routes)
            addDynamicRoutes(routes, 'Layout', router)
            isAddDynamicRoute = true
            console.log(router.getRoutes())
            next({...to, replace: true})
        }

    }

}

const addDynamicRoutes = (routes: any[], parentName = 'Layout', router: Router) => {
    const allDynamicComponents = import.meta.glob("../../views/**/*.vue", {eager: false})
    routes.forEach(route => {
        const component = allDynamicComponents[`../../views/${route.component}.vue`]
        // 构造 Vue Router 格式的路由
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
            parentName = route.name!
            addDynamicRoutes(route.children, route.name!, router)
        }
    })
}