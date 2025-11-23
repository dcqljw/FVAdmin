import {createRouter, createWebHistory} from 'vue-router'
import {staticRoutes} from "@/router/routes/staticRoutes.ts";
import {setupBeforeEachGuard} from "@/router/guards/beforeEach.ts";
import type {App} from "vue";


export const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: staticRoutes
})

export function initRouter(app: App<Element>): void {
    setupBeforeEachGuard(router)
    app.use(router)
}
