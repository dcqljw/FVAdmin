import type {App} from "vue";
import {createPinia} from "pinia";
import {createPersistedState} from "pinia-plugin-persistedstate";

export const store = createPinia();

store.use(
    createPersistedState({
        storage: localStorage,
    })
)

export function initStore(app: App<Element>): void {
    app.use(store);
}