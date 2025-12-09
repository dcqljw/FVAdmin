import type {RouteRecordRaw} from "vue-router";

export const staticRoutes: RouteRecordRaw[] = [
    {
        path: "/login",
        name: "Login",
        component: () => import('@/views/LoginView.vue')
    }, {
        path: "/",
        name: "Layout",
        component: () => import('@/layout/index.vue'),
        children: [
            {
                path: "/user_info",
                name: "user_info",
                meta: {
                    title: "个人中心",
                },
                component: () => import('@/views/UserInfoView.vue')
            }
        ]
    }
]